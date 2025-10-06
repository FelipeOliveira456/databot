import re

def extract_json_block(text: str) -> str:
    match = re.search(r"```json(.*?)```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Não foi possível encontrar um bloco JSON no texto fornecido.")
    return match.group(1).strip()