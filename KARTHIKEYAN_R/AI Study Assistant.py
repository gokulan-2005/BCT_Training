import ollama

# Assistant Agent (generates answer)
def assistant_agent(question):
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response['message']['content']


# Critic Agent (improves answer)
def critic_agent(answer):
    prompt = f"Improve this answer and make it very simple:\n{answer}"
    
    response = ollama.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']


# Main Program (Agent Workflow)
if __name__ == "__main__":
    question = input("Enter your question: ")

    print("\n🧠 Thinking...\n")

    # Assistant generates answer
    answer = assistant_agent(question)

    # Critic improves it
    final_answer = critic_agent(answer)

    # Output
    print("🧠 Assistant Answer:\n")
    print(answer)

    print("\n🔍 Improved Answer:\n")
    print(final_answer)