from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(
    "mysql+pymysql://root:root%40123@localhost:3306/ai_analytics"
)

def execute_query(sql):
    try:
        return db.run(sql)
    except Exception as e:
        return f"SQL Error: {str(e)}"