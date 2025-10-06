from databot.graph.workflow import create_databot_graph

app = create_databot_graph()

def run_databot(msg: str, csv_path: str = None):
    first_state = {
        "input": msg
    }
    if csv_path:
        first_state["csv_path"] = csv_path
    
    return app.invoke(first_state)