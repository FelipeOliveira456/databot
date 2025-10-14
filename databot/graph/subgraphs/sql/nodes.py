from typing import Any
from langchain_core.runnables import RunnableWithFallbacks
from langchain_core.messages import AIMessage
from databot.tools.sql import (
    list_sql_database_tool,
    info_sql_database_tool,
    query_sql_database
)
from databot.agents.sql import (
    get_query_gen,
)
from langgraph.prebuilt import ToolNode
from databot.schemas.schemas import (
    BaseState as State,
)
from databot.graph.subgraphs.sql.utils import extract_sql_block

def create_list_tables_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return ToolNode([list_sql_database_tool])

def create_info_table_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return ToolNode([info_sql_database_tool])

def sql_db_schema_node(state: State):
    content = state["messages"][-1].content
    table_names = content.strip()        
    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "sql_db_schema",
                        "args": {"table_names": table_names},
                        "id": "tool_schema_001",
                    }
                ],
            )
        ],
    }


def first_tool_call_node(state: State):
    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "sql_db_list_tables",
                        "args": {},
                        "id": "tool_abcd123",
                    }
                ],
            )
        ],
    }

query_gen = get_query_gen()

def query_gen_node(state: State):
    question = state["messages"][0].content
    schema = state["messages"][4].content

    attempts = state["messages"][5::2]
    error_msgs = state["messages"][6::2]

    errors = ""
    for attempt, error in zip(attempts, error_msgs):
        errors += f"Tentativa falha:\n{attempt.content}\n\n"
        errors += f"Erro recebido:\n{error.content}\n\n"

    output = query_gen.invoke({
        "schema": schema,
        "question": question,
        "errors": errors.strip()
    })

    return {"messages": [output]}

def execute_query_node(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    content = last_message.content

    try:
        query = extract_sql_block(content)
    except:
        return {"messages": "Erro: Não foi possível extrair uma consulta SQL da resposta. Corrija e tente novamente."}

    if not query:
        return {"messages": "Erro: A consulta SQL está vazia."}

    try:
        query_sql_database(query)
        return {"messages": query}
    except RuntimeError as e:
        return {"messages": f'{e}'}
