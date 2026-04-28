def clean_sql(query):
    return query.replace("```sql", "").replace("```", "").strip()