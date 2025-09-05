from chatbot.schemas.schemas import (
    RAGSchemaState as State
)
from chatbot.graph.subgraphs.rag.utils import get_schema_vectorstore

def get_retriever_node(state: State):
    schema = state['schema']
    vector_store = get_schema_vectorstore(schema)
    retriever = vector_store.as_retriever()
    question = state['question']
    documents = retriever.invoke(question)
    concatenated_text = "\n\n".join(doc.page_content for doc in documents)
    return {'documents': concatenated_text}
