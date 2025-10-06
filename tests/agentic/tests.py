import json
import re
from pathlib import Path

from databot.agents.databot import get_task_agent
from llm import get_task_evaluator_agent_simple  

questions_path = Path("questions.json")
results_path = Path("results.json")
accuracy_path = Path("accuracy.json")

task_agent = get_task_agent()
evaluator_agent = get_task_evaluator_agent_simple()

with questions_path.open("r", encoding="utf-8") as f:
    questions = json.load(f)

all_results = []

accuracy_list = []

for i in range(5):
    print(i)
    results = []

    acc = 0

    for q in questions:
        csv_file = q.get("csv", "")
        if csv_file:
            csv_file = Path(csv_file)


        user_message = q.get("question", "")

        task_state = {
            "user_message": user_message,
            "user_csv": csv_file
        }

        predicted_output = task_agent.invoke(task_state)
        predicted_content = predicted_output.content
        pattern = r"```json\s*(\{.*?\})\s*```"
        match = re.search(pattern, predicted_content, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = ""

        try:
            predicted_tasks = json.loads(json_str).get("tasks", [])
        except Exception:
            predicted_tasks = []

        correct_tasks = q.get("tasks", [])

        eval = 0

        predicted_subgraphs = [t.get("subgraph") for t in predicted_tasks]
        correct_subgraphs = [t.get("subgraph") for t in correct_tasks]

        if predicted_subgraphs == correct_subgraphs:

            eval_state = {
                "gold_tasks": json.dumps(correct_tasks, ensure_ascii=False),
                "predicted_tasks": json.dumps(predicted_tasks, ensure_ascii=False)
            }

            eval = evaluator_agent.invoke(eval_state).content

            try:
                eval = int(eval.strip())
            except ValueError:
                eval = 0

            eval = eval/10 

        result_entry = {
            "question": user_message,
            "csv": str(csv_file) if csv_file else "",
            "correct_tasks": correct_tasks,
            "predicted_tasks": predicted_tasks,
            "evaluate": eval
        }

        acc += eval

        results.append(result_entry)
    
    all_results.append(results)

    accuracy_list.append(acc/len(results))

with results_path.open("w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

average_accuracy = sum(accuracy_list) / len(accuracy_list)

accuracy_total = {
    "accuracy_per_execution": accuracy_list,
    "average_accuracy": average_accuracy
}

with accuracy_path.open("w", encoding="utf-8") as f:
    json.dump(accuracy_total, f, ensure_ascii=False, indent=2)


