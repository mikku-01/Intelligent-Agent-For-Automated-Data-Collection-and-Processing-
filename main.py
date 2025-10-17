from typing import List, Dict, Any, Optional
import autogen
from crewai import Agent, Task, Crew
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from config.settings import OPENAI_API_KEY, AGENT_CONFIG, REVIEW_CONFIG
from agents.specialized.collector_agent import DataCollectorAgent
from agents.specialized.processor_agent import DataProcessorAgent
from agents.specialized.storage_agent import DataStorageAgent
import logging
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IntelligentAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        
        # Initialize specialized agents
        self.collector = DataCollectorAgent(AGENT_CONFIG["collector"])
        self.processor = DataProcessorAgent(AGENT_CONFIG["processor"])
        self.storage = DataStorageAgent(AGENT_CONFIG["storage"])
        
        # Initialize scheduler for periodic tasks
        self.scheduler = BackgroundScheduler()
        self._setup_scheduled_tasks()
        
        # Start the scheduler
        self.scheduler.start()
        
    def _setup_scheduled_tasks(self):
        """Set up periodic tasks."""
        # Check for data updates every hour
        self.scheduler.add_job(
            self._check_for_updates,
            'interval',
            hours=1,
            id='data_update_check'
        )
        
        # Process review queue every 4 hours
        self.scheduler.add_job(
            self._process_review_queue,
            'interval',
            hours=4,
            id='review_queue_processing'
        )
    
    async def process_data_source(self, source: Dict[str, Any], review_required: bool = True) -> Dict[str, Any]:
        """
        Process a single data source using the specialized agents.
        
        Args:
            source: Dictionary containing source information
            review_required: Whether human review is required for this source
        
        Returns:
            Dictionary containing processing results and metadata
        """
        try:
            # Step 1: Collect data
            collection_result = self.collector.collect_data(source)
            if collection_result["status"] != "success":
                return collection_result
            
            # Step 2: Process collected data
            processing_result = self.processor.process_data(collection_result)
            if processing_result["status"] != "success":
                return processing_result
            
            # Check if review is needed
            needs_review = (
                review_required and
                processing_result.get("needs_review", False)
            )
            
            # Auto-approve if quality metrics are above threshold
            quality_score = processing_result.get("quality_metrics", {}).get("completeness", 0)
            if needs_review and quality_score >= REVIEW_CONFIG["auto_approve_threshold"]:
                needs_review = False
                logger.info(f"Auto-approved data from {source} (quality score: {quality_score})")
            
            # Step 3: Store processed data
            storage_result = self.storage.store_data(processing_result)
            
            result = {
                "status": "success",
                "source": source,
                "collected_at": collection_result.get("collected_at"),
                "processed_at": processing_result.get("processed_at"),
                "stored_at": storage_result.get("stored_at"),
                "entry_id": storage_result.get("entry_id"),
                "needs_review": needs_review,
                "quality_metrics": processing_result.get("quality_metrics"),
                "metadata": {
                    "content_hash": collection_result.get("metadata", {}).get("content_hash"),
                    "content_length": collection_result.get("metadata", {}).get("content_length"),
                    "entities_found": len(processing_result.get("entities", [])),
                    "validation_failures": len(processing_result.get("validation_results", {}).get("failures", [])),
                    "anomaly_score": processing_result.get("anomalies", {}).get("anomaly_score", 0)
                }
            }
            
            logger.info(f"Successfully processed source: {source}")
            return result
            
        except Exception as e:
            error_msg = f"Error processing data source {source}: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "source": source,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    async def run(self, sources: List[Dict[str, Any]], parallel: bool = True) -> List[Dict[str, Any]]:
        """
        Run the intelligent agent on multiple data sources.
        
        Args:
            sources: List of data source configurations
            parallel: Whether to process sources in parallel
        
        Returns:
            List of processing results
        """
        results = []
        
        if parallel:
            # Process sources in parallel using asyncio
            import asyncio
            tasks = [self.process_data_source(source) for source in sources]
            results = await asyncio.gather(*tasks)
        else:
            # Process sources sequentially
            for source in sources:
                result = await self.process_data_source(source)
                results.append(result)
                
        return results
    
    async def _check_for_updates(self):
        """Periodic task to check for data updates."""
        logger.info("Checking for data updates...")
        # Implementation of update checking logic
    
    async def _process_review_queue(self):
        """Periodic task to process the review queue."""
        logger.info("Processing review queue...")
        pending_reviews = self.storage.get_pending_reviews()
        
        for review in pending_reviews:
            # Check if review has expired
            review_age = datetime.now() - datetime.fromisoformat(review["collected_at"])
            if review_age.total_seconds() / 3600 > REVIEW_CONFIG["review_expiration_hours"]:
                # Auto-approve expired reviews
                self.storage.update_review_status(
                    review["id"],
                    "auto_approved_expired",
                    "system"
                )
                logger.info(f"Auto-approved expired review for entry {review['id']}")
    
    def get_review_queue(self) -> List[Dict[str, Any]]:
        """Get the current review queue."""
        return self.storage.get_pending_reviews()
    
    def approve_review(self, entry_id: int, reviewer: str) -> bool:
        """Approve a pending review."""
        return self.storage.update_review_status(entry_id, "approved", reviewer)
    
    def reject_review(self, entry_id: int, reviewer: str, reason: str) -> bool:
        """Reject a pending review."""
        return self.storage.update_review_status(entry_id, f"rejected: {reason}", reviewer)
    
    def get_data_by_id(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve stored data by ID."""
        return self.storage.get_data_by_id(entry_id)

if __name__ == "__main__":
    # Example usage
    agent = IntelligentAgent()
    
    # Define data sources
    sources = [
        {
            "type": "website",
            "url": "https://example.com/data"
        },
        {
            "type": "api",
            "endpoint": "https://api.example.com/data",
            "params": {"key": "value"}
        }
    ]
    
    # Run the agent
    results = agent.run(sources)
    print(json.dumps(results, indent=2))
