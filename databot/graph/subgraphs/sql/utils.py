from langgraph.graph import END
from databot.schemas.schemas import BaseState as State
from typing import Literal
import re

def router(state: State) -> Literal[END, "query_gen_agent"]:
    last_message = state["messages"][-1].content

    if last_message.startswith("Erro"):
        return "query_gen_agent"
    return END

def extract_sql_block(content) -> str | None:
    """
    Extrai a query SQL que está dentro de um bloco ```sql na última mensagem.
    Retorna a query ou None se não encontrar.
    """

    match = re.search(r"```sql\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None