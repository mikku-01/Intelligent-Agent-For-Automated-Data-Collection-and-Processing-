from agents.core_agent import agent

# Example: Use the agent to scrape a website, process it, extract entities, and store
task_prompt = """
Go to https://www.example.com, scrape the main content, clean and transform the data,
extract named entities, and store the processed data in the database.
"""

try:
    agent.run(task_prompt)
except Exception as e:
    print(f"Agent execution failed: {e}")
