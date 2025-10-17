import requests
import json
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class RateLimitedAPIClient:
    """
    API client with intelligent rate limiting and error handling.
    """
    
    def __init__(self, rate_limit: int = 10, time_window: int = 60):
        """
        Initialize the API client.
        
        Args:
            rate_limit: Maximum number of requests per time window
            time_window: Time window in seconds
        """
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_times = defaultdict(list)
        self.session = requests.Session()
    
    def _check_rate_limit(self, endpoint: str) -> bool:
        """Check if we're within rate limits for the endpoint."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)
        
        # Remove old request times
        self.request_times[endpoint] = [
            t for t in self.request_times[endpoint] if t > cutoff
        ]
        
        # Check if we can make another request
        if len(self.request_times[endpoint]) < self.rate_limit:
            self.request_times[endpoint].append(now)
            return True
        
        # Calculate wait time
        oldest_request = min(self.request_times[endpoint])
        wait_time = (oldest_request + timedelta(seconds=self.time_window) - now).total_seconds()
        logger.info(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
        time.sleep(wait_time + 0.1)
        
        return self._check_rate_limit(endpoint)
    
    def call_api(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        data: Optional[Dict] = None,
        retry_attempts: int = 3
    ) -> Dict[str, Any]:
        """
        Make an API call with rate limiting and error handling.
        
        Args:
            endpoint: The API endpoint URL
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            headers: Request headers
            data: Request body data
            retry_attempts: Number of retry attempts
            
        Returns:
            Dictionary containing the API response or error information
        """
        # Check rate limit
        self._check_rate_limit(endpoint)
        
        last_error = None
        for attempt in range(retry_attempts):
            try:
                response = self.session.request(
                    method=method,
                    url=endpoint,
                    params=params,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                # Handle different status codes
                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json() if response.content else {},
                        "status_code": response.status_code,
                        "headers": dict(response.headers)
                    }
                elif response.status_code == 429:  # Too Many Requests
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited by server. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.Timeout as e:
                last_error = f"Timeout: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} timed out for {endpoint}")
            except requests.exceptions.RequestException as e:
                last_error = f"Request error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} failed for {endpoint}: {str(e)}")
            
            if attempt < retry_attempts - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
        
        return {
            "success": False,
            "error": last_error,
            "endpoint": endpoint
        }
    
    def batch_call(self, endpoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Make multiple API calls with rate limiting.
        
        Args:
            endpoints: List of endpoint configurations
            
        Returns:
            List of API responses
        """
        results = []
        for config in endpoints:
            result = self.call_api(**config)
            results.append(result)
        return results

# Backward compatibility function
def call_api(endpoint: str, params: dict = None, headers: dict = None) -> dict:
    """
    Simple API call function for backward compatibility.
    
    Args:
        endpoint: The API endpoint URL
        params: Query parameters
        headers: Request headers
        
    Returns:
        Dictionary containing the API response or error
    """
    try:
        client = RateLimitedAPIClient()
        result = client.call_api(endpoint, params=params, headers=headers)
        
        if result["success"]:
            return result["data"]
        else:
            return {"error": result.get("error", "Unknown error")}
    except Exception as e:
        return {"error": str(e)}
