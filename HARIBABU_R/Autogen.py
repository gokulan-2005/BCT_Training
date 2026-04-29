from autogen_agentchat import AssistantAgent, UserProxyAgent
import pandas as pd
import os

df = pd.read_csv("resume_dataset.csv")


config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    }
]

llm_config = {
    "config_list": config_list
}
parser = AssistantAgent(
    name="ResumeParser",
    system_message="Extract skills, experience, and domain from resume.",
    llm_config=llm_config
)

matcher = AssistantAgent(
    name="JobMatcher",
    system_message="Match candidate with job role and explain suitability.",
    llm_config=llm_config
)

ranker = AssistantAgent(
    name="RankingAgent",
    system_message="Give score (1-10) and reason.",
    llm_config=llm_config
)

user = UserProxyAgent(name="HR_Manager")

# Job role
job_role = "Data Scientist with Python, Machine Learning, NLP"

# Process dataset
for i, row in df.iterrows():

    print("\n==========================")
    print(f"Candidate {i+1}")
    print("==========================")

    resume_text = row['Resume']

    
    user.initiate_chat(
        parser,
        message=f"Extract details from:\n{resume_text}"
    )

    
    parser.initiate_chat(
        matcher,
        message=f"Match with job role: {job_role}\nResume:\n{resume_text}"
    )

    
    matcher.initiate_chat(
        ranker,
        message="Provide score and justification."
    )