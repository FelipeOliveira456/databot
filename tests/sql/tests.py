from databot.graph.subgraphs.sql.workflow import create_sql_graph
import json
from pathlib import Path
from databot.tools.sql import query_sql_database

current_dir = Path(__file__).parent
questions_file = current_dir / "questions.json"

with open(questions_file, "r", encoding="utf-8") as f:
    questions_data = json.load(f)

app = create_sql_graph()

accuracy_list = []

all_results = []

for _ in range(10):

    totals = {"facil": 0, "media": 0, "dificil": 0}
    corrects = {"facil": 0, "media": 0, "dificil": 0}

    results = []

    for item in questions_data:
        difficulty = item["difficulty"]

        totals[difficulty] += 1

        pergunta = item["question"]

        first_state = {"messages": pergunta}
        try:
            result = app.invoke(first_state)
            response = result["messages"][-1].content.replace("\n", " ").strip() 
            correct_sql = query_sql_database(item["answer"])
            predict_sql = query_sql_database(response)
            correct_set_frozenset = set(frozenset(t) for t in correct_sql)
            predict_set_frozenset = set(frozenset(t) for t in predict_sql)
            if correct_set_frozenset == predict_set_frozenset:
                corrects[difficulty] += 1

        except Exception as e:
            pass 

        results.append({"question": pergunta, "answer": response})
        all_results.append(results)


    accuracy_by_difficulty = {
        diff: (corrects[diff] / totals[diff] if totals[diff] > 0 else 0.0)
        for diff in totals
    }

    accuracy_list.append(accuracy_by_difficulty)

output_file = current_dir / "results.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

average_accuracy = {
    diff: sum(run[diff] for run in accuracy_list) / len(accuracy_list)
    for diff in ["facil", "media", "dificil"]
}

accuracy_total = {
    "accuracy_per_execution": accuracy_list,
    "average_accuracy": average_accuracy
}

accuracy_file = current_dir / "accuracy.json"

with open(accuracy_file, "w", encoding="utf-8") as f:
    json.dump(accuracy_total, f, ensure_ascii=False, indent=4)


