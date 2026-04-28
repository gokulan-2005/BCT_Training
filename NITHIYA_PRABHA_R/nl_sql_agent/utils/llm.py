from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return "groq/llama-3.1-8b-instant"
    