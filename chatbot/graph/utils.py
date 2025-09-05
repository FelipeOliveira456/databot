from typing import (
    Literal, 
)
from chatbot.schemas.schemas import(
    SupervisorState as State,
    Task
)
from langgraph.graph import END
import json
import re
import os
import uuid
import pandas as pd

CSV_DIR = os.path.expanduser("~/Documents/chatbot/chatbot/data/csv")
os.makedirs(CSV_DIR, exist_ok=True)

def route_next(state: State) -> Literal["sql_graph", "analysis_graph", END]:
    actual_task = state.get("task", None)
    if(actual_task is None):
        return END
    subgraph = actual_task.get("subgraph", "")

    print(f"Roteando para subgraph: {subgraph}")

    if subgraph == "sql":
        return "sql_graph"
    elif subgraph == "analysis":
        return "analysis_graph"
    else: 
        return END

def extract_summary_from_response(response) -> str:
    try:
        data = json.loads(response.content)
        return data.get("summary", "")
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Erro ao extrair resumo: {e}")
        return ""
    
def format_task(task: dict) -> str:
    if not task:
        return "Nenhuma task atual."
    subgraph = task.get("subgraph", "desconhecido")
    description = task.get("description", "sem descrição")
    return f"Subgrafo: {subgraph}, Descrição: {description}"

def format_messages(messages: list[dict]) -> str:
    if not messages:
        return "Sem mensagens anteriores."
    
    formatted = []
    for i, msg in enumerate(messages):
        role = getattr(msg, "role", "desconhecido")  # usa getattr
        content = msg.content
        formatted.append(f"{role.capitalize()} {i+1}: {content}")
    return "\n".join(formatted)

def extract_json_block(text: str) -> str:
    match = re.search(r"```json(.*?)```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Não foi possível encontrar um bloco JSON no texto fornecido.")
    return match.group(1).strip()

def save_df_to_csv(df: pd.DataFrame) -> str:
    file_name = f"{uuid.uuid4().hex}.csv"
    file_path = os.path.join(CSV_DIR, file_name)
    df.to_csv(file_path, index=False)
    print(file_path)
    return file_path