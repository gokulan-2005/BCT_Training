from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from config import MODEL_NAME

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0
)

def generate_answer(question, result):
    prompt = PromptTemplate(
        input_variables=["question", "result"],
        template="""
        Question: {question}
        SQL Result: {result}

        Convert this into a simple answer.
        """
    )

    response = llm.invoke(prompt.format(
        question=question,
        result=result
    ))

    return response.content