from crewai import Crew, Task

from agents.analyzer import analyzer
from agents.sql_generator import sql_generator
from agents.reporter import reporter

from utils.db import execute_query


def create_crew(user_query):

    analyze_task = Task(
        description=f"Analyze this query and understand intent: {user_query}",
        agent=analyzer,
        expected_output="Clear explanation of what user wants"
    )

    sql_task = Task(
        description=f"""
        Based on the user query: "{user_query}"
        
        Generate a valid MySQL SQL query.
        Use tables: customers, orders, order_items, products
        
        IMPORTANT:
        - Return ONLY SQL query
        - No markdown
        - No explanation
        """,
        agent=sql_generator,
        expected_output="Pure SQL query"
    )

    def execute_and_format(task_output):
        sql_query = task_output.raw.strip()

        result = execute_query(sql_query)

        return f"""
        SQL Query:
        {sql_query}

        Result:
        {result}
        """

    report_task = Task(
        description="Execute SQL and return final answer",
        agent=reporter,
        expected_output="Final result",
        callback=execute_and_format
    )

    crew = Crew(
        agents=[analyzer, sql_generator, reporter],
        tasks=[analyze_task, sql_task, report_task],
        verbose=True,
        tracing=True
    )

    return crew