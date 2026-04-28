from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from .tools import scrape_website, search_google_news, save_markdown_article

load_dotenv()

MODEL = "gemini-2.5-flash-lite"

def retrieve_news_agent(topic):
    return Agent(
        role=f"{topic} AI News Retriever",
        goal=f"Find recent, relevant reporting about {topic}",
        backstory="Expert researcher",
        llm=MODEL,
        tools=[search_google_news, scrape_website],
        verbose=True,
        allow_delegation=False,
    )

def writer_agent():
    return Agent(
        role="News Writer",
        goal="Write a factual markdown news brief",
        backstory="Expert journalist",
        llm=MODEL,
        tools=[save_markdown_article],
        verbose=True,
        allow_delegation=False,
    )

def run_crew(topic):
    retriever = retrieve_news_agent(topic)
    writer = writer_agent()

    task1 = Task(
        description=(
            f"Research {topic} with the available search tool, then scrape the strongest 3 to 5 direct article URLs. "
            "Return structured research notes with article title, URL, publisher, and concise fact bullets from the scraped content. "
            "Prefer reputable publishers and skip any result you cannot scrape."
        ),
        expected_output="Structured research notes with direct URLs and scraped fact bullets.",
        agent=retriever,
    )

    task2 = Task(
        description=(
            f"Write a markdown article about {topic} using only the scraped notes. "
            "Include a title, short overview, key developments, and a source list. "
            "If facts conflict or are unclear, say so instead of guessing. "
            f"After writing the article, save it with the save_markdown_article tool using topic '{topic}' and return the article plus saved path."
        ),
        expected_output="A markdown article and the saved .md file path.",
        agent=writer,
        context=[task1],
    )

    crew = Crew(
        agents=[retriever, writer],
        tasks=[task1, task2],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    saved_path = save_markdown_article.run(content=str(result), topic=topic)
    return f"{result}\n\n{saved_path}"
