from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model=os.getenv("MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL"),

    model_info={
        "family": "unknown",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,  
    },
)