import os
from dotenv import load_dotenv

load_dotenv()

config_list = [
    {
        "model": "llama-3.1-8b-instant",  
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.2
}