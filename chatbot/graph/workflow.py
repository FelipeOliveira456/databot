from chatbot.graph.nodes import (
    supervisor_node,
    sql_node
)
from chatbot.schemas.schemas import(
    BaseState as State,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from chatbot.graph.utils import (
    route_next
)

def create_chatbot_graph():

    chatbot_workflow = StateGraph(State)
    thread_memory = MemorySaver()

    chatbot_workflow.add_node("supervisor_agent",supervisor_node)
    chatbot_workflow.add_node("sql_graph", sql_node)

    chatbot_workflow.add_edge(START, "supervisor_agent")
    chatbot_workflow.add_conditional_edges(
        "supervisor_agent",
        route_next
    )
    chatbot_workflow.add_edge("sql_graph", "supervisor_agent")

    app = chatbot_workflow.compile(checkpointer=thread_memory)

    return app
    

# arestas = create_chatbot_graph().get_graph().edges
# for aresta in arestas:
#     print(aresta)

# from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

# def generate_and_save_png():
#     # Cria o chatbot_graph
#     app = create_chatbot_graph()  # Isso cria o grafo de estados
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








    
