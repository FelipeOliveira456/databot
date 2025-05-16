from pydantic import BaseModel, Field
from typing import Literal

class RouteSupervisor(BaseModel):
    """
    Decision router between agent nodes.

    This tool is used to determine the next step in the conversation flow
    and to define the message to be passed to another agent (e.g., an SQL agent).

    Use this tool only when the message is not intended for the human user
    interacting with the chatbot. If the message should go to the human,
    do not use this tool—respond directly instead.
    """
    goto: Literal["sql"] = Field(
        ...,
        description="Target destination. Use 'sql' to forward to the SQL agent."
    )
    message: str = Field(
        ...,
        description="Message to be sent to the next agent based on the chosen destination."
    )
