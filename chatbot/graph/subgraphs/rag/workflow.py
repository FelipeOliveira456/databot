from chatbot.graph.subgraphs.rag.nodes import (
    get_retriever_node
)
from langgraph.graph import StateGraph, START, END
from chatbot.schemas.schemas import (
    RAGSchemaState
)

def create_rag_node():
    rag_node = StateGraph(RAGSchemaState)

    rag_node.add_node("retriever_agent", get_retriever_node)

    rag_node.add_edge(START, "retriever_agent")
    rag_node.add_edge("retriever_agent", END)

    app = rag_node.compile()
    return app 