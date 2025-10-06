from databot.graph.workflow import create_databot_graph
import json
from pathlib import Path
import shutil

current_dir = Path(__file__).parent

questions_file = current_dir / "questions.json"
csv_dir = current_dir / "data/csv"
pdf_dir = current_dir / "data/pdf"
img_dir = current_dir / "data/img"

csv_dir.mkdir(parents=True, exist_ok=True)
pdf_dir.mkdir(parents=True, exist_ok=True)
img_dir.mkdir(parents=True, exist_ok=True)

with open(questions_file, "r", encoding="utf-8") as f:
    questions_data = json.load(f)  # lista de perguntas

app = create_databot_graph()

for i, question in enumerate(questions_data, start=1):
    print(i)
    first_state = {
        "input": question
    }

    try:
        result = app.invoke(first_state)

        # Mover CSV gerado
        csv_path = result.get("csv_path")
        if csv_path:
            shutil.move(str(csv_path), str(csv_dir / f"{i}.csv"))

        # Mover PDF gerado
        pdf_path = result.get("pdf_path")
        if pdf_path:
            shutil.move(str(pdf_path), str(pdf_dir / f"{i}.pdf"))

        img_plots = result.get("plots", [])
        for j, plot in enumerate(img_plots):
            img_path = img_dir / f"{i}.{j}.png"
            shutil.move(str(plot["path"]), str(img_path))

    except Exception as e:
        print(f"Erro ao processar pergunta {i}: {e}")
