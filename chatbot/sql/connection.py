from langchain_community.utilities import SQLDatabase

DB_URI = "sqlite:///Chinook.db"  
db = SQLDatabase.from_uri(DB_URI)

def get_db():
    return db