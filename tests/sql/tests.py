from chatbot.graph.subgraphs.sql.workflow import create_sql_graph
import json
from pathlib import Path

current_dir = Path(__file__).parent
questions_file = current_dir / "questions.json"

with open(questions_file, "r", encoding="utf-8") as f:
    questions_data = json.load(f)


app = create_sql_graph()


