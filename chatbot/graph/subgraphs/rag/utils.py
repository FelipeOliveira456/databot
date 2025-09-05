from langchain_community.vectorstores import Chroma
from chatbot.agents.rag import embed_model
from langchain.schema import Document

def get_schema_vectorstore(schema):
    create_tables = split_create_tables_by_double_newline(schema)

    documents = [Document(page_content=table) for table in create_tables]

    vectorstore = Chroma.from_documents(
        documents=documents,
        collection_name="schema-rag",
        embedding=embed_model,
    )

    return vectorstore

def split_create_tables_by_double_newline(sql_code: str) -> list[str]:
    parts = sql_code.strip().split('\n\n')
    create_tables = [p for p in parts if p.strip().upper().startswith("CREATE TABLE")]
    return create_tables