from databot.sql.connection import get_db
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)

db = get_db()
list_sql_database_tool = ListSQLDatabaseTool(db=db)
info_sql_database_tool = InfoSQLDatabaseTool(db=db)

def query_sql_database(query: str) -> str:
    prohibited_commands = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
    
    query_upper = query.upper()

    if any(cmd in query_upper for cmd in prohibited_commands):
        raise RuntimeError("Comandos que modificam o banco de dados não são permitidos.")

    try:
        result = db.run(query)
    except Exception as e:
        raise RuntimeError(f"Erro ao executar a consulta SQL: {e}")

    return result