import os
from dotenv import load_dotenv
from crew import SmartShoppingCrew


load_dotenv()

def run():
    """
    Kicks off the Smart Shopping Assistant Crew.
    """
   
    inputs = {
        'product_name': 'Mechanical Keyboards',
        'price_range': 'under $100'
    }
    
    print("--- Starting the Smart Shopping Crew ---")
    
    try:
  
        result = SmartShoppingCrew().crew().kickoff(inputs=inputs)
        
        print("\n\n########################")
        print("## FINAL RECOMMENDATION ##")
        print("########################\n")
        print(result)
        
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()