from langgraph.graph import END
from chatbot.schemas.schemas import BaseState as State
from typing import Literal

def router(state: State) -> Literal[END, "query_gen_agent"]:
    last_message = state["messages"][-1].content

    if last_message.startswith("Erro"):
        return "query_gen_agent"
    return END

# def ordenar_tabelas_por_fk(schema_sql: dict[str, str]) -> list[str]:
#     def contar_fk(ddl: str) -> int:
#         return len(re.findall(r'FOREIGN KEY', ddl))

#     fk_counts = {tabela: contar_fk(ddl) for tabela, ddl in schema_sql.items()}

#     ordenados = sorted(fk_counts, key=lambda t: fk_counts[t], reverse=True)

#     return ordenados