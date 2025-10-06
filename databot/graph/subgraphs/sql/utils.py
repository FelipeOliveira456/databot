from langgraph.graph import END
from databot.schemas.schemas import BaseState as State
from typing import Literal

def router(state: State) -> Literal[END, "query_gen_agent"]:
    last_message = state["messages"][-1].content

    if last_message.startswith("Erro"):
        return "query_gen_agent"
    return END