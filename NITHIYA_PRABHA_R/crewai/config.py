from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(model="tinyllama")  #lightweight model