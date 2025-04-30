from langchain_core.tools import tool
from sql.connection import get_db
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)
from pydantic import BaseModel, Field
from typing import List, Any

db = get_db()
list_sql_database_tool = ListSQLDatabaseTool(db=db)
info_sql_database_tool = InfoSQLDatabaseTool(db=db)

@tool
def query_sql_database_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result

class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to orchestrator that will process this data"""

    final_answer: List[List[Any]] = Field(..., description="The final answer to orchestrator")
    description: str = Field(..., description="Summary of what the final_answer data contains, including columns and context.")


