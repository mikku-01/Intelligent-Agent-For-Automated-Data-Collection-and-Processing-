from typing import Dict, Any, Optional
import autogen
from langchain.agents import Tool
from modules.collector.web_scraper import scrape_website
from modules.collector.api_client import call_api
import json
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataCollectorAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.tools = self._initialize_tools()
        self.data_cache = {}  # Cache for incremental processing
        
    def _initialize_tools(self) -> list:
        return [
            Tool(
                name="WebScraper",
                func=scrape_website,
                description="Scrape website content with automatic layout adaptation"
            ),
            Tool(
                name="APICaller",
                func=call_api,
                description="Call API endpoints with error handling and rate limiting"
            )
        ]
    
    def _calculate_content_hash(self, content: str) -> str:
        """Calculate hash of content for change detection."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format and accessibility."""
        import re
        from urllib.parse import urlparse
        
        # Basic URL format validation
        if not url:
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def collect_data(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect data from a source with validation and change detection.
        
        Args:
            source: Dictionary containing source information and configuration
            
        Returns:
            Dictionary containing collected data and metadata
        """
        try:
            source_type = source.get("type", "").lower()
            source_url = source.get("url") or source.get("endpoint")
            
            if not self._validate_url(source_url):
                raise ValueError(f"Invalid URL: {source_url}")
            
            # Check cache for previous content hash
            previous_hash = self.data_cache.get(source_url)
            
            # Collect data based on source type
            if source_type == "website":
                content = scrape_website(source_url)
            elif source_type == "api":
                content = json.dumps(call_api(
                    source_url,
                    params=source.get("params"),
                    headers=source.get("headers")
                ))
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            # Calculate new content hash
            current_hash = self._calculate_content_hash(content)
            
            # Check if content has changed
            if current_hash == previous_hash:
                logger.info(f"No changes detected for source: {source_url}")
                return {
                    "status": "unchanged",
                    "source_url": source_url,
                    "last_check": datetime.now().isoformat()
                }
            
            # Update cache
            self.data_cache[source_url] = current_hash
            
            # Prepare result with metadata
            result = {
                "status": "success",
                "source_url": source_url,
                "source_type": source_type,
                "collected_at": datetime.now().isoformat(),
                "content": content,
                "metadata": {
                    "content_hash": current_hash,
                    "content_length": len(content),
                    "is_changed": previous_hash is not None
                }
            }
            
            logger.info(f"Successfully collected data from {source_url}")
            return result
            
        except Exception as e:
            error_msg = f"Error collecting data from {source.get('url', 'unknown source')}: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "source_url": source.get("url"),
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_collection_status(self, source_url: str) -> Optional[Dict[str, Any]]:
        """Get the current collection status for a source."""
        return {
            "url": source_url,
            "last_hash": self.data_cache.get(source_url),
            "is_tracked": source_url in self.data_cache
        }