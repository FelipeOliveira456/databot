from langgraph.graph.message import AnyMessage, add_messages
from typing import Annotated, Any
from langchain_core.runnables import RunnableWithFallbacks
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, ToolMessage
from tools.utils import create_tool_node_with_fallback
from tools.sql_tools import (
    list_sql_database_tool,
    info_sql_database_tool,
    query_sql_database_tool,
)
from agents.sql_agents import (
    get_query_checker,
    get_schema_model,
    get_query_gen
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def create_list_tables_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([list_sql_database_tool])

def create_info_table_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([info_sql_database_tool])

def create_query_executor_tool_node() -> RunnableWithFallbacks[Any, dict]:
    return create_tool_node_with_fallback([query_sql_database_tool])

def first_tool_call_node(state: State) -> dict[str, list[AIMessage]]:
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
    message = query_gen.invoke(state)

    tool_messages = []
    if message.tool_calls:
        for tc in message.tool_calls:
            if tc["name"] != "SubmitFinalAnswer":
                tool_messages.append(
                    ToolMessage(
                        content=f"Error: The wrong tool was called: {tc['name']}. Please fix your mistakes. Remember to only call SubmitFinalAnswer to submit the final answer. Generated queries should be outputted WITHOUT a tool call.",
                        tool_call_id=tc["id"],
                    )
                )
    else:
        tool_messages = []
    return {"messages": [message] + tool_messages}

query_check = get_query_checker()

def check_query_node(state: State) -> dict[str, list[AIMessage]]:
    """
    Use this tool to double-check if your query is correct before executing it.
    """
    return {"messages": [query_check.invoke({"messages": [state["messages"][-1]]})]}