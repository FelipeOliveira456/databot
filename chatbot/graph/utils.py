from typing import Literal
from langchain_core.messages import AIMessage
from chatbot.schemas.schemas import(
    BaseState as State
)
from langgraph.graph import END

def route_next(state: State) -> Literal["human_agent", "sql_graph", END]:
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    if len(tool_calls) == 0:
        if "/quit" in last_message.content:
            return END
        return "human_agent"

    tool_call = tool_calls[0]
    next_message = tool_call["args"]["message"]
    state["messages"][-1] = AIMessage(next_message)
    return "sql_graph"
