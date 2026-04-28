def is_safe(query: str):
    blocked = ["drop", "delete", "update", "insert", "alter"]
    return not any(word in query.lower() for word in blocked)