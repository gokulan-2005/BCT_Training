import time
import logging
from crewai import Crew
from litellm.exceptions import RateLimitError
from db import init_db
from agents import *
from tasks import create_tasks   

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run(user_id: str):  
    logging.info("Initializing database...")
    init_db()

    tasks = create_tasks(user_id)

    crew = Crew(
        agents=[credit_agent, income_agent, risk_agent, decision_agent],
        tasks=tasks,
        process="sequential",
        verbose=False
    )

    MAX_RETRIES = 3
    RETRY_WAIT = 25

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Starting Crew execution (Attempt {attempt}) for user: {user_id}")
            result = crew.kickoff()
            logging.info("Execution completed successfully")
            print("\nFINAL RESULT:\n", result)
            return result

        except RateLimitError:
            logging.warning("Rate limit hit")

            if attempt < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_WAIT} seconds...")
                time.sleep(RETRY_WAIT)
            else:
                logging.error("Max retries reached. Exiting")
                raise

        except Exception as e:
            logging.exception("Unexpected error occurred")
            raise e


if __name__ == "__main__":
    user_id = input("Enter USER_ID: ").strip()

    if not user_id:
        print("USER_ID cannot be empty")
    else:
        run(user_id)