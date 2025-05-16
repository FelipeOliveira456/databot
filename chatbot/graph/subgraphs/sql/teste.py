from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from typing import Annotated, Any, Literal

class SubmitAnswerToUser(BaseModel):
    """Submit the final answer to user"""
    final_answer: str = Field(..., description="Human readable response to user")

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["hilda", "sql", "plot", "FINISH"]

llm = ChatOllama(model="gemma:2b", temperature=0).bind_tools(
    [SubmitAnswerToUser]
)

messages = ["give-me the query plot graph"]

response = llm.with_structured_output(Router).invoke(messages)


print(response)