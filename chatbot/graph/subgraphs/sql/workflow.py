from chatbot.graph.subgraphs.sql.nodes import (
    create_list_tables_tool_node,
    create_info_table_tool_node,
    create_query_executor_tool_node,
    first_tool_call_node,
    get_schema_node,
    query_gen_node,
)
from langgraph.graph import StateGraph, START
from chatbot.schemas.schemas import (
    BaseState as State
)
from chatbot.graph.subgraphs.sql.utils import router

def create_sql_graph():

    sql_workflow = StateGraph(State)

    sql_workflow.add_node("first_tool_call", first_tool_call_node)
    sql_workflow.add_node("list_tables_tool", create_list_tables_tool_node())
    sql_workflow.add_node("get_schema_agent", get_schema_node)
    sql_workflow.add_node("get_schema_tool", create_info_table_tool_node())
    sql_workflow.add_node("query_gen_agent", query_gen_node)
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
    sql_workflow.add_edge("execute_query_tool", "query_gen_agent")

    app = sql_workflow.compile()

    return app

# arestas = create_sql_graph().get_graph().edges
# for aresta in arestas:
#     print(aresta)

# from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
# 
# def generate_and_save_png():
#     # Cria o chatbot_graph
#     app = create_sql_graph()  # Isso cria o grafo de estados
#     graph = app.get_graph(xray=1)  # Obtém o grafo
    
#     # Gerando o gráfico no formato PNG
#     graph_png = graph.draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)    
#     # Salvando o PNG em um arquivo
#     output_png = "chatbot_graph_atualizado.png"
#     with open(output_png, "wb") as f:
#         f.write(graph_png)
    
#     print(f"Grafo gerado e salvo em formato PNG: {output_png}")

# # Chame a função para gerar o arquivo PNG
# generate_and_save_png()

