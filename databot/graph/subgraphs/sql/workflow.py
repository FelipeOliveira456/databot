from databot.graph.subgraphs.sql.nodes import (
    create_list_tables_tool_node,
    create_info_table_tool_node,
    first_tool_call_node,
    query_gen_node,
    sql_db_schema_node,
    execute_query_node,
)
from langgraph.graph import StateGraph, START
from databot.schemas.schemas import (
    BaseState as State
)
from databot.graph.subgraphs.sql.utils import router

def create_sql_graph():

    sql_workflow = StateGraph(State)

    sql_workflow.add_node("first_tool_call", first_tool_call_node)
    sql_workflow.add_node("list_tables_tool", create_list_tables_tool_node())
    sql_workflow.add_node("schema_tool_call", sql_db_schema_node)
    sql_workflow.add_node("get_schema_tool", create_info_table_tool_node())
    sql_workflow.add_node("query_gen_agent", query_gen_node)
    sql_workflow.add_node("execute_query_tool", execute_query_node)

    sql_workflow.add_edge(START, "first_tool_call")
    sql_workflow.add_edge("first_tool_call", "list_tables_tool")
    sql_workflow.add_edge("list_tables_tool", "schema_tool_call")
    sql_workflow.add_edge("schema_tool_call", "get_schema_tool")
    sql_workflow.add_edge("get_schema_tool", "query_gen_agent")
    sql_workflow.add_edge("query_gen_agent", "execute_query_tool")
    sql_workflow.add_conditional_edges(
        "execute_query_tool",
        router,
    )

    app = sql_workflow.compile()

    return app

