from databot.graph.nodes import (
    router_node,
    sql_node,
    analysis_node,
    task_node,
    change_task_node
)
from databot.schemas.schemas import(
    SupervisorState as State,
)
from langgraph.graph import END, StateGraph, START
from databot.graph.utils import (
    route_next
)

def create_databot_graph():

    databot_workflow = StateGraph(State)

    databot_workflow.add_node("task_agent", task_node)
    databot_workflow.add_node("router",router_node)
    databot_workflow.add_node("change_task", change_task_node)
    databot_workflow.add_node("sql_graph", sql_node)
    databot_workflow.add_node("analysis_graph", analysis_node)

    databot_workflow.add_edge(START, "task_agent")
    databot_workflow.add_edge("task_agent", "router")
    databot_workflow.add_conditional_edges(
        "router",
        route_next
    )
    databot_workflow.add_edge("sql_graph", "change_task")
    databot_workflow.add_edge("analysis_graph", "change_task")
    databot_workflow.add_edge("change_task", "router")

    app = databot_workflow.compile()

    return app








    
