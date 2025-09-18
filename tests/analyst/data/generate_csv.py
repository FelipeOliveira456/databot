import json
from pathlib import Path
import pandas as pd
from chatbot.sql.connection import get_db
import os

def save_df_to_csv(df: pd.DataFrame, n: int) -> str:
    file_name = f"{n}.csv"
    file_path = os.path.join("./csv", file_name)
    df.to_csv(file_path, index=False)
    print(file_path)
    return file_path

db = get_db()

current_dir = Path(__file__).parent
questions_file = current_dir / "sql.json"

with open(questions_file, "r", encoding="utf-8") as f:
    queries_data = json.load(f)

for i, query in enumerate(queries_data, start=1):
    df = pd.read_sql(query, db._engine)
    csv_path = save_df_to_csv(df=df, n=i)
    df.to_csv(csv_path, index=False)

