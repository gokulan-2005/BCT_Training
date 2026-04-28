from pandasai import SmartDataframe
from app.groq_llm import GroqLLM


def analyze(df, query):
    try:
        llm = GroqLLM()

        sdf = SmartDataframe(df, config={
            "llm": llm,
            "verbose": True,
            "max_retries": 1,
            "save_charts": True,
            "save_charts_path": "charts"
        })

        result = sdf.chat(query)

        # ✅ Ensure safe return
        return result

    except Exception as e:
        return f"Error: {str(e)}"