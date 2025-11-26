import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama

load_dotenv()

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Please enter your PostgreSQL connection string.")
        print("Format: postgresql://user:password@localhost:5432/dbname")
        db_url = input("Connection String: ").strip()
    return db_url

def get_llm():
    model_name = os.getenv("OLLAMA_MODEL", "llama3")
    print(f"Initializing Ollama with model: {model_name}")
    return ChatOllama(model=model_name, temperature=0)

def main():
    print("--- SQL Query Agent ---")
    
    # Setup Database
    db_uri = get_db_connection()
    try:
        db = SQLDatabase.from_uri(db_uri)
        print("Connected to database.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    # Setup LLM
    llm = get_llm()

    # Create Agent with improved error handling
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="zero-shot-react-description",
        max_iterations=10,
        max_execution_time=60,
        handle_parsing_errors="Check your output and make sure it conforms to the expected format!",
        verbose=True
    )

    print("\nAgent ready! Enter your query (or 'exit' to quit).")
    
    while True:
        user_query = input("\nQuery: ").strip()
        if user_query.lower() in ['exit', 'quit', 'q']:
            break
        
        if not user_query:
            continue
            
        try:
            # The agent handles the chain: Thought -> Action -> Observation -> Answer
            response = agent_executor.invoke({"input": user_query})
            print(f"\nResult: {response['output']}")
        except Exception as e:
            print(f"\nError processing query: {e}")

if __name__ == "__main__":
    main()
