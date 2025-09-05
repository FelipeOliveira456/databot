from chatbot.sql.connection import get_db
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)
from pydantic import BaseModel, Field
from typing import Literal
import re
from langchain_core.output_parsers import PydanticOutputParser

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

# class RelevantSchema(BaseModel):
#     relevant: Literal["sim", "nao"] = Field(..., description="Indica se o schema é relevante para a pergunta")
#     explain: str = Field(..., description="Explicação do motivo da relevância ou irrelevância")


# class CleanThinkParser(PydanticOutputParser):
#     def parse_result(self, text: str):
#         cleaned_text = re.sub(r"<think>.*?</think>", "", text[0].text, flags=re.DOTALL).strip()
#         text[0].text = cleaned_text
#         return super().parse_result(text)
