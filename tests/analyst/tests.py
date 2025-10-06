from databot.graph.subgraphs.analysis.workflow import create_analysis_graph
import json
from pathlib import Path
import pandas as pd
import shutil

current_dir = Path(__file__).parent

questions_file = current_dir / "questions.json"
csv_dir = current_dir / "data/csv"
pdf_dir = current_dir / "data/pdf"
img_dir = current_dir / "data/img"

with open(questions_file, "r", encoding="utf-8") as f:
    questions_data = json.load(f)

app = create_analysis_graph()

results = []

for question in questions_data:
    q = question["pergunta"]
    csv_name = question["csv"]
    csv_path = csv_dir / csv_name
    df = pd.read_csv(csv_path)
    first_state = {
        "input": q,
        "df": df
    }
    try:
        result = app.invoke(first_state)
        old_pdf_path = result["pdf_path"]
        question_number = next((c for c in csv_name if c.isdigit()), None)

        new_pdf_path = pdf_dir / f"{question_number}.pdf" 
        shutil.move(str(old_pdf_path), str(new_pdf_path))
        img_plots = result["plots"]
        for i, plot in enumerate(img_plots):
            img_path = img_dir / f"{question_number}.{i}.png"
            path = plot["path"]
            shutil.move(str(path), str(img_path))
        results.append({
            "nome_pdf": f"{question_number}.pdf",
            "avaliacao": ""
        })
    except:
        results.append({
            "nome_pdf": f"{question_number}.pdf",
            "avaliacao": "Erro ao gerar relatório"
        })

results_path = current_dir / "results.json"

with open(results_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"Resultados salvos em {results_path}")

