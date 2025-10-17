from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from config import settings
from modules.collector.web_scraper import scrape_website
from modules.collector.api_client import call_api
from modules.processor.data_cleaner import clean_data
from modules.processor.nlp_extractor import extract_entities
from modules.storage.database_manager import store_data

# Initialize OpenAI LLM
llm = OpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)

# Define tools
tools = [
    Tool(name="WebScraper", func=scrape_website, description="Scrape website content from a URL"),
    Tool(name="APICaller", func=call_api, description="Call API endpoint and get JSON data"),
    Tool(name="DataProcessor", func=clean_data, description="Clean and transform raw data"),
    Tool(name="EntityExtractor", func=extract_entities, description="Extract named entities from text"),
    Tool(name="DataStorage", func=store_data, description="Store processed data into database")
]

# Initialize agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
