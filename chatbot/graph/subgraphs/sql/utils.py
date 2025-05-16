from langgraph.graph import END
from chatbot.schemas.schemas import BaseState as State
from typing import Literal

def router(state: State) -> Literal[END, "query_gen_agent", "check_query_agent"]:
    messages = state["messages"]
    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return END
    if last_message.content.startswith("Error:"):
        return "query_gen_agent"
    else:
        return "check_query_agent"