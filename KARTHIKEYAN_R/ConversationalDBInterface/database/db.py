from langchain_community.utilities import SQLDatabase
def get_db():
    return SQLDatabase.from_uri("sqlite:///database/sample.db")