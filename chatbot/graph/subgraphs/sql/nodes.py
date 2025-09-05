from typing import Any
from langchain_core.runnables import RunnableWithFallbacks
from langchain_core.messages import AIMessage, RemoveMessage, ToolMessage
from chatbot.tools.sql import (
    list_sql_database_tool,
    info_sql_database_tool,
    query_sql_database
)
from chatbot.agents.sql import (
    get_query_gen,
)
from langgraph.prebuilt import ToolNode
from chatbot.schemas.schemas import (
    BaseState as State,
)
from chatbot.sql.connection import get_db
import re

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

# schema_judger = get_schema_judger()
# db = get_db()

# def get_judger_node(state: State):
#     table_names_str = state["messages"][-1].content.strip()
#     question = state["question"]
#     print(question)

#     table_names = [name.strip() for name in table_names_str.split(',') if name.strip()]

#     schema_sql = {}

#     for table in table_names:
#         schema = info_sql_database_tool._run(table)
#         schema_sql[table] = schema

#     ordenados = ordenar_tabelas_por_fk(schema_sql)

#     relevants = []
#     accepted_schemas = []

#     for table in ordenados:
#         schema_result = schema_sql[table] 

#         schemas_to_judge = ""

#         if accepted_schemas:
#             schemas_to_judge += "Schemas já aceitos:\n"
#             schemas_to_judge += "\n\n".join(accepted_schemas)
#             schemas_to_judge += "\n\n"

#         schemas_to_judge += f"Schema a ser avaliado agora:\nTabela: {table}\n{schema_result}"

#         input = {
#             "question": question,
#             "schema": schemas_to_judge
#         }

#         result = schema_judger.invoke(input)
#         print(result)

#         if "sim" in result.relevant.lower():
#             accepted_schemas.append(f"Table: {table}\n{schema_result}")
#             relevants.append(table)

#     relevant_tables = ", ".join(relevants)

#     return {
#         "messages": [
#             AIMessage(
#                 content="",
#                 tool_calls=[
#                     {
#                         "name": "sql_db_schema",
#                         "args": {"table_names": relevant_tables},
#                         "id": "tool_schema_123"
#                     }
#                 ]
#             )
#         ]
#     }

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

    match = re.search(r"```(?:sql|json)?\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)
    if not match:
        return {"messages": "Erro: Não foi possível extrair uma consulta SQL da resposta. Corrija e tente novamente."}
    
    query = match.group(1).strip()

    if not query:
        return {"messages": "Erro: A consulta SQL está vazia."}

    try:
        query_sql_database(query)
        return {"messages": query}
    except RuntimeError as e:
        return {"messages": f'{e}'}


# def rag_node(state: State):
#     retriever_node = create_rag_node()
#     schema = state["messages"][-1].content
#     question = state["messages"][-5].content
#     input_data = {
#         'question': question,
#         'schema': schema
#     }
#     response = retriever_node.invoke(input_data)
#     tool_message = {
#         "role": "tool",
#         "name": "sql_db_schema", 
#         "tool_call_id": 'tool_id_140',  
#         "content": response['documents']
#     }
#     return {"messages": [tool_message]}

# def delete_messages_node(state: State):
#     messages = state["messages"]
#     schema = str(messages[-1].content)
#     return {"schema": schema, "messages": [RemoveMessage(id=m.id) for m in messages]}