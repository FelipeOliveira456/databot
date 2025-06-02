from langchain_core.tools import tool
from chatbot.sql.connection import get_db
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
    Execute uma consulta SQL no banco de dados e obtenha o resultado.
    Se a consulta não estiver correta, uma mensagem de erro será retornada.
    Se um erro for retornado, reescreva a consulta, verifique-a e tente novamente.
    """

    result = db.run_no_throw(query)
    if not result:
        return "Erro: A consulta falhou. Por favor, reescreva sua consulta e tente novamente."
    return result

