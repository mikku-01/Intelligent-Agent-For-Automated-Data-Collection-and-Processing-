import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional, List
import time
import logging
from urllib.parse import urljoin, urlparse
import json

logger = logging.getLogger(__name__)

class SelfHealingScraper:
    """
    Web scraper with self-healing capabilities to adapt to website changes.
    """
    
    def __init__(self, retry_attempts: int = 3, timeout: int = 30):
        self.retry_attempts = retry_attempts
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.selectors_cache = {}
    
    def scrape_with_retry(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Scrape website with retry logic and adaptive selector finding.
        
        Args:
            url: The URL to scrape
            selectors: Optional CSS selectors for specific elements
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        last_error = None
        
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content
                content = self._extract_content(soup, selectors)
                
                # Extract metadata
                metadata = self._extract_metadata(soup, url)
                
                return {
                    "success": True,
                    "url": url,
                    "content": content,
                    "metadata": metadata,
                    "status_code": response.status_code
                }
                
            except requests.RequestException as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return {
            "success": False,
            "url": url,
            "error": str(last_error)
        }
    
    def _extract_content(self, soup: BeautifulSoup, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Extract content using provided selectors or intelligent defaults."""
        content = {}
        
        if selectors:
            # Use provided selectors
            for key, selector in selectors.items():
                elements = soup.select(selector)
                content[key] = [elem.get_text(strip=True) for elem in elements]
        else:
            # Intelligent content extraction
            content = {
                "title": soup.find('title').get_text(strip=True) if soup.find('title') else "",
                "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
                "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
                "links": [a.get('href') for a in soup.find_all('a', href=True)],
                "main_text": soup.get_text(separator=' ', strip=True)
            }
        
        return content
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract metadata from the page."""
        metadata = {
            "url": url,
            "domain": urlparse(url).netloc
        }
        
        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                metadata[name] = content
        
        return metadata
    
    def scrape_multiple_pages(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape multiple URLs efficiently."""
        results = []
        for url in urls:
            result = self.scrape_with_retry(url)
            results.append(result)
            time.sleep(1)  # Be respectful with rate limiting
        return results

# Backward compatibility function
def scrape_website(url: str) -> str:
    """
    Simple scraping function for backward compatibility.
    
    Args:
        url: The URL to scrape
        
    Returns:
        Scraped text content or error message
    """
    try:
        scraper = SelfHealingScraper()
        result = scraper.scrape_with_retry(url)
        
        if result["success"]:
            return result["content"].get("main_text", "")
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error: {e}"
