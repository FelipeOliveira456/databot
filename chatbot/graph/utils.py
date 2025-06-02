from typing import Literal
from chatbot.schemas.schemas import(
    BaseState as State
)
from langgraph.graph import END

def route_next(state: State) -> Literal["sql_graph", END]:
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    if len(tool_calls) == 0:
        return END

    return "sql_graph"
