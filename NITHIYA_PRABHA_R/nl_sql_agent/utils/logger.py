def log_query(question, answer):
    with open("logs/log.txt", "a") as f:
        f.write(f"Q: {question}\nA: {answer}\n\n")