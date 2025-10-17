import asyncio
from main import IntelligentAgent
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_run():
    try:
        # Initialize the agent
        agent = IntelligentAgent()
        
        # Define test sources
        test_sources = [
            {
                "type": "website",
                "url": "https://example.com"
            },
            {
                "type": "api",
                "endpoint": "https://api.example.com/data",
                "params": {"key": "value"}
            }
        ]
        
        # Run the agent
        logger.info("Starting agent test run...")
        results = await agent.run(test_sources, parallel=True)
        
        # Print results
        logger.info("Test run results:")
        print(json.dumps(results, indent=2))
        
        # Check review queue
        reviews = agent.get_review_queue()
        if reviews:
            logger.info(f"Found {len(reviews)} items in review queue:")
            print(json.dumps(reviews, indent=2))
        
    except Exception as e:
        logger.error(f"Error during test run: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_run())