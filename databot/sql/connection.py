from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("MYSQL_DB")

mysql_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=0)

def get_db():
    return db
