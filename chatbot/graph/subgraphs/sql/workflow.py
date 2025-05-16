from chatbot.graph.subgraphs.sql.nodes import (
    create_list_tables_tool_node,
    create_info_table_tool_node,
    create_query_executor_tool_node,
    first_tool_call_node,
    get_schema_node,
    query_gen_node,
    check_query_node
)
from langgraph.graph import END, StateGraph, START
from chatbot.schemas.schemas import BaseState as State
from chatbot.graph.subgraphs.sql.utils import router

def create_sql_graph():

    sql_workflow = StateGraph(State)

    sql_workflow.add_node("first_tool_call", first_tool_call_node)
    sql_workflow.add_node("list_tables_tool", create_list_tables_tool_node())
    sql_workflow.add_node("get_schema_agent", get_schema_node)
    sql_workflow.add_node("get_schema_tool", create_info_table_tool_node())
    sql_workflow.add_node("query_gen_agent", query_gen_node)
    sql_workflow.add_node("check_query_agent", check_query_node)
    sql_workflow.add_node("execute_query_tool", create_query_executor_tool_node())

    sql_workflow.add_edge(START, "first_tool_call")
    sql_workflow.add_edge("first_tool_call", "list_tables_tool")
    sql_workflow.add_edge("list_tables_tool", "get_schema_agent")
    sql_workflow.add_edge("get_schema_agent", "get_schema_tool")
    sql_workflow.add_edge("get_schema_tool", "query_gen_agent")
    sql_workflow.add_conditional_edges(
        "query_gen_agent",
        router,
    )
    sql_workflow.add_edge("check_query_agent", "execute_query_tool")
    sql_workflow.add_edge("execute_query_tool", "query_gen_agent")

    app = sql_workflow.compile()

    return app

