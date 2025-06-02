from typing import Any
from langchain_core.runnables import RunnableWithFallbacks
from langchain_core.messages import AIMessage
from chatbot.tools.utils import create_tool_node_with_fallback
from chatbot.tools.sql import (
    list_sql_database_tool,
    info_sql_database_tool,
    query_sql_database_tool,
)
from chatbot.agents.sql import (
    get_schema_model,
    get_query_gen
)

from chatbot.schemas.schemas import (
    BaseState as State,
)

def create_list_tables_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([list_sql_database_tool])

def create_info_table_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([info_sql_database_tool])

def create_query_executor_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([query_sql_database_tool])

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
        ]
    }

schema_model = get_schema_model()

def get_schema_node(state: State):
    return {"messages": [schema_model.invoke(state["messages"])]}

query_gen = get_query_gen()

def query_gen_node(state: State):
    return {"messages": query_gen.invoke({"messages": state["messages"]})}
