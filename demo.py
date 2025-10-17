"""
Demo Script - Test Intelligent Agent Without External APIs

This script demonstrates the agent capabilities using mock data
so you can test the system without needing API keys or external services.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List

# Mock data for testing
MOCK_WEBSITE_DATA = """
<html>
<head><title>Sample News Site</title></head>
<body>
    <h1>Breaking News</h1>
    <h2>Technology Update</h2>
    <p>Artificial intelligence continues to transform industries worldwide.</p>
    <p>New advances in machine learning enable better automation.</p>
    <h2>Business Section</h2>
    <p>Companies like Microsoft and Google are investing heavily in AI research.</p>
    <p>The global AI market is expected to reach $500 billion by 2025.</p>
</body>
</html>
"""

MOCK_API_DATA = {
    "data": [
        {"id": 1, "name": "Product A", "price": 29.99, "category": "Electronics"},
        {"id": 2, "name": "Product B", "price": 49.99, "category": "Electronics"},
        {"id": 3, "name": "Product C", "price": 19.99, "category": "Books"},
    ],
    "total": 3,
    "page": 1
}

class MockCollector:
    """Mock data collector for demo purposes."""
    
    def collect_data(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate data collection."""
        print(f"📥 Collecting data from: {source.get('url', source.get('endpoint'))}")
        
        if source.get("type") == "website":
            content = MOCK_WEBSITE_DATA
        elif source.get("type") == "api":
            content = json.dumps(MOCK_API_DATA)
        else:
            content = "Sample text data for testing."
        
        return {
            "status": "success",
            "source_url": source.get("url", source.get("endpoint")),
            "source_type": source.get("type"),
            "collected_at": datetime.now().isoformat(),
            "content": content,
            "metadata": {
                "content_hash": "mock_hash_123",
                "content_length": len(content),
                "is_changed": True
            }
        }

class MockProcessor:
    """Mock data processor for demo purposes."""
    
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate data processing."""
        print(f"⚙️  Processing data from: {data.get('source_url')}")
        
        # Simulate data cleaning
        content = data.get("content", "")
        cleaned_data = content.replace("<html>", "").replace("</html>", "").strip()
        
        # Simulate quality metrics
        quality_metrics = {
            "completeness": 0.95,
            "uniqueness": 0.88,
            "consistency": 0.92
        }
        
        # Simulate validation
        validation_results = {
            "failures": [],
            "warnings": ["No email validation performed (mock mode)"]
        }
        
        # Simulate anomaly detection
        anomalies = {
            "anomaly_score": 0.15,
            "anomalous_rows": []
        }
        
        # Simulate entity extraction
        entities = [
            {"text": "Microsoft", "label": "ORG"},
            {"text": "Google", "label": "ORG"},
            {"text": "2025", "label": "DATE"}
        ]
        
        return {
            "status": "success",
            "source_url": data.get("source_url"),
            "processed_at": datetime.now().isoformat(),
            "processed_data": {"cleaned_content": cleaned_data[:200] + "..."},
            "entities": entities,
            "quality_metrics": quality_metrics,
            "validation_results": validation_results,
            "anomalies": anomalies,
            "needs_review": quality_metrics["completeness"] < 0.8
        }

class MockStorage:
    """Mock data storage for demo purposes."""
    
    def __init__(self):
        self.stored_data = []
    
    def store_data(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate data storage."""
        print(f"💾 Storing data from: {processed_data.get('source_url')}")
        
        entry_id = len(self.stored_data) + 1
        processed_data["entry_id"] = entry_id
        self.stored_data.append(processed_data)
        
        return {
            "status": "success",
            "stored_at": datetime.now().isoformat(),
            "entry_id": entry_id,
            "needs_review": processed_data.get("needs_review", False)
        }
    
    def get_all_stored_data(self) -> List[Dict[str, Any]]:
        """Get all stored data."""
        return self.stored_data

class DemoAgent:
    """Demo agent that uses mock components."""
    
    def __init__(self):
        self.collector = MockCollector()
        self.processor = MockProcessor()
        self.storage = MockStorage()
    
    async def process_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single data source."""
        print(f"\n{'='*60}")
        print(f"Processing source: {source}")
        print(f"{'='*60}")
        
        # Step 1: Collect
        collection_result = self.collector.collect_data(source)
        if collection_result["status"] != "success":
            return collection_result
        
        # Step 2: Process
        processing_result = self.processor.process_data(collection_result)
        if processing_result["status"] != "success":
            return processing_result
        
        # Step 3: Store
        storage_result = self.storage.store_data(processing_result)
        
        return {
            "status": "success",
            "source": source,
            "entry_id": storage_result["entry_id"],
            "quality_metrics": processing_result["quality_metrics"],
            "entities_found": len(processing_result["entities"]),
            "needs_review": storage_result["needs_review"]
        }
    
    async def run(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run the demo agent on multiple sources."""
        results = []
        for source in sources:
            result = await self.process_source(source)
            results.append(result)
            await asyncio.sleep(0.5)  # Simulate processing time
        return results

async def main():
    """Main demo function."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Intelligent Agent Demo - Mock Data Testing             ║
    ║                                                           ║
    ║   This demo uses mock data to demonstrate agent          ║
    ║   capabilities without requiring external APIs           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize demo agent
    agent = DemoAgent()
    
    # Define test sources
    sources = [
        {
            "type": "website",
            "url": "https://example-news.com/tech"
        },
        {
            "type": "api",
            "endpoint": "https://api.example.com/products"
        },
        {
            "type": "website",
            "url": "https://example-blog.com/ai-trends"
        }
    ]
    
    # Run the agent
    print("\n🚀 Starting data collection and processing...\n")
    results = await agent.run(sources)
    
    # Display results
    print(f"\n{'='*60}")
    print("📊 RESULTS SUMMARY")
    print(f"{'='*60}\n")
    
    for i, result in enumerate(results, 1):
        print(f"Source {i}: {result['source'].get('url', result['source'].get('endpoint'))}")
        print(f"  Status: {result['status']}")
        print(f"  Entry ID: {result.get('entry_id')}")
        print(f"  Quality Metrics:")
        for metric, value in result.get('quality_metrics', {}).items():
            print(f"    - {metric}: {value:.2%}")
        print(f"  Entities Found: {result.get('entities_found')}")
        print(f"  Needs Review: {result.get('needs_review')}")
        print()
    
    # Show stored data
    print(f"{'='*60}")
    print("💾 STORED DATA")
    print(f"{'='*60}\n")
    print(f"Total entries stored: {len(agent.storage.get_all_stored_data())}")
    
    print("\n✅ Demo completed successfully!")
    print("\nNext steps:")
    print("1. Configure your .env file with real API keys")
    print("2. Run: python test_run.py (for real data processing)")
    print("3. Check docs/project_guide.md for full documentation")
    print()

if __name__ == "__main__":
    asyncio.run(main())