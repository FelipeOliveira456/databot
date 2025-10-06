from databot.agents.databot import (
    get_task_agent
)
from databot.utils import extract_json_block
from databot.graph.utils import (
    save_df_to_csv
)
from databot.schemas.schemas import ( 
    DataAnalysisState,
    SupervisorState
)
from databot.graph.subgraphs.sql.workflow import create_sql_graph
from databot.sql.connection import get_db
from databot.graph.subgraphs.analysis.workflow import create_analysis_graph
from databot.schemas.schemas import Task
import pandas as pd
import json

task_agent = get_task_agent()
sql_graph = create_sql_graph()
analysis_graph = create_analysis_graph()
db = get_db()

def task_node(state: SupervisorState):
    user_message = state.get("input", "")
    csv = state.get("csv_path", "")

    response = task_agent.invoke({
        "user_message": user_message,
        "user_csv": csv
    })

    json_str = extract_json_block(response.content)
    print(json_str)

    tasks_data = json.loads(json_str)
    tasks_raw = tasks_data.get("tasks", [])
    tasks_list: list[Task] = [Task(subgraph=t["subgraph"], description=t["description"]) for t in tasks_raw]

    current_task = tasks_list[0] if tasks_list else None
    remaining_tasks = tasks_list[1:] if len(tasks_list) > 1 else []

    return {
        **state,
        "task": current_task,
        "tasks_list": remaining_tasks
    }

def router_node(state: SupervisorState):
    return {
        **state,
    }

def change_task_node(state: SupervisorState):
    tasks_list = state.get("tasks_list", [])
    new_task = tasks_list[0] if tasks_list else None
    remaining_tasks = tasks_list[1:] if len(tasks_list) > 1 else []

    return {
        **state,
        "task": new_task,
        "tasks_list": remaining_tasks
    }

def sql_node(state: SupervisorState):
    actual_task = state.get("task", "")
    message = actual_task.get("description", "")

    first_state = {"messages": message}
    result = sql_graph.invoke(first_state)

    response = result["messages"][-1]
    query_sql = response.content

    print(query_sql)

    try:
        df = pd.read_sql(query_sql, db._engine)
        csv_path = save_df_to_csv(df=df)
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"Erro ao executar query SQL ou salvar CSV: {e}")
        df = pd.DataFrame()
        csv_path = save_df_to_csv(df=df)

    return {
        **state,
        "csv_path": csv_path,
    }

def analysis_node(state: SupervisorState):
    csv_path = state.get("csv_path", None)

    df = pd.read_csv(csv_path)

    actual_task = state.get("task", "")
    message = actual_task.get("description", "")

    first_state: DataAnalysisState = {
        "input": message,
        "df": df
    }

    result = analysis_graph.invoke(first_state)
    pdf_path = result.get("pdf_path", "")
    markdown = result.get("markdown", "")

    return {
        **state,
        "pdf_path": pdf_path,
        "markdown": markdown
    }

    