from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableBinding
from langchain_core.runnables.base import RunnableSequence
from chatbot.tools.sql import (
    info_sql_database_tool,
    query_sql_database_tool,
)
from langchain_ollama import ChatOllama

def get_schema_model() -> RunnableBinding:
    model_get_schema = ChatOllama(model="qwen2.5-coder:14b", temperature=0).bind_tools(
        [info_sql_database_tool]
    )

    return model_get_schema
    
def get_query_gen() -> RunnableSequence:
    query_gen_system = """
    Você é um agente de geração de SQL conectado a um banco de dados MySQL.

    Sua tarefa é:
    1. Traduzir a pergunta do usuário, escrita em linguagem natural, para uma consulta SQL válida.
    2. Chamar a ferramenta `query_sql_database_tool` com essa consulta para executá-la.
    3. Após receber o resultado da consulta, enviar ao ususário o resultado da query.

    Regras:
    - NÃO responda à pergunta antes de executar a consulta.
    - SEMPRE use a ferramenta `query_sql_database_tool` para executar a consulta.
    - Sua resposta final deve se basear estritamente no resultado real da consulta — não invente nem assuma dados.
    - Se o usuário não especificar quantos resultados deseja, limite o conjunto de resultados a no máximo 5 linhas.
    - NÃO selecione todas as colunas (evite `SELECT *`). Inclua apenas as colunas relevantes para a pergunta.
    - NUNCA escreva consultas que modifiquem o banco de dados (sem INSERT, UPDATE, DELETE, DROP, etc).
    """

    query_gen_prompt = ChatPromptTemplate.from_messages(
        [("system", query_gen_system), ("placeholder", "{messages}")]
    )
    query_gen = query_gen_prompt | ChatOllama(model="qwen2.5-coder:14b", temperature=0).bind_tools(
        [query_sql_database_tool]
    )

    return query_gen
