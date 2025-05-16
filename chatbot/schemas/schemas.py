from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict

class BaseState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    summary: str


