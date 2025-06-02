from langgraph.graph import END
from chatbot.schemas.schemas import BaseState as State
from typing import Literal

def router(state: State) -> Literal[END, "execute_query_tool"]:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return END
    else:
        return "execute_query_tool"