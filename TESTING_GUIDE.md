# 🧪 Testing Guide - Intelligent Agent Project

## Testing Options Overview

There are 4 ways to test this project, from easiest to most advanced:

```
1. Demo Mode (No setup) ⭐ START HERE
2. Unit Tests (Verify components)
3. Integration Tests (Full pipeline)
4. Real Data Tests (With API keys)
```

---

## 1️⃣ Demo Mode - Instant Testing (Recommended!)

**No installation or API keys required!**

### Run the Demo
```bash
python demo.py
```

### What It Does
- ✅ Uses mock data (no external APIs)
- ✅ Tests all three agents (Collector, Processor, Storage)
- ✅ Shows quality metrics and entity extraction
- ✅ Demonstrates the complete pipeline
- ✅ Takes ~5 seconds to complete

### Expected Output
```
╔═══════════════════════════════════════════════════════════╗
║   Intelligent Agent Demo - Mock Data Testing             ║
╚═══════════════════════════════════════════════════════════╝

🚀 Starting data collection and processing...

📥 Collecting data from: https://example-news.com/tech
⚙️  Processing data from: https://example-news.com/tech
💾 Storing data from: https://example-news.com/tech

📊 RESULTS SUMMARY
Source 1: https://example-news.com/tech
  Status: success
  Entry ID: 1
  Quality Metrics:
    - completeness: 95.00%
    - uniqueness: 88.00%
    - consistency: 92.00%
  Entities Found: 3
  Needs Review: False

✅ Demo completed successfully!
```

---

## 2️⃣ Unit Tests - Component Testing

### Prerequisites
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Run All Tests
```bash
# Basic run
pytest tests/

# Verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=. --cov-report=html

# Specific test file
pytest tests/test_agents.py -v

# Single test function
pytest tests/test_agents.py::test_collector_url_validation -v
```

### Test Structure
```
tests/
├── test_agents.py          # Agent integration tests
├── test_collector.py       # Collector agent tests
├── test_processor.py       # Processor agent tests
└── test_storage.py         # Storage agent tests
```

### Create Additional Tests
```python
# tests/test_custom.py
import pytest

def test_my_feature():
    # Your test here
    assert True
```

---

## 3️⃣ Integration Tests - Full Pipeline

### Manual Integration Test

Create a file `integration_test.py`:

```python
import asyncio
from agents.specialized.collector_agent import DataCollectorAgent
from agents.specialized.processor_agent import DataProcessorAgent
from agents.specialized.storage_agent import DataStorageAgent
from config.settings import AGENT_CONFIG

async def test_full_pipeline():
    """Test the complete data processing pipeline."""
    
    # Initialize agents
    collector = DataCollectorAgent(AGENT_CONFIG["collector"])
    processor = DataProcessorAgent(AGENT_CONFIG["processor"])
    storage = DataStorageAgent(AGENT_CONFIG["storage"])
    
    # Test data source
    source = {
        "type": "website",
        "url": "https://example.com"
    }
    
    print("Step 1: Collecting data...")
    collection_result = collector.collect_data(source)
    assert collection_result["status"] == "success"
    print(f"✓ Collection status: {collection_result['status']}")
    
    print("\nStep 2: Processing data...")
    processing_result = processor.process_data(collection_result)
    assert processing_result["status"] == "success"
    print(f"✓ Processing status: {processing_result['status']}")
    print(f"✓ Quality metrics: {processing_result['quality_metrics']}")
    
    print("\nStep 3: Storing data...")
    storage_result = storage.store_data(processing_result)
    assert storage_result["status"] == "success"
    print(f"✓ Storage status: {storage_result['status']}")
    print(f"✓ Entry ID: {storage_result['entry_id']}")
    
    print("\n✅ Full pipeline test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
```

Run it:
```bash
python integration_test.py
```

---

## 4️⃣ Real Data Tests - Production Testing

### Prerequisites
1. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. Configure `.env`:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. Verify configuration:
```bash
python -c "from config.settings import OPENAI_API_KEY; print('API Key:', 'configured' if OPENAI_API_KEY else 'missing')"
```

### Run Real Data Test

Use the provided `test_run.py`:

```bash
python test_run.py
```

### Custom Real Data Test

Create `real_test.py`:

```python
import asyncio
from main import IntelligentAgent

async def test_real_sources():
    """Test with real data sources."""
    
    agent = IntelligentAgent()
    
    # Define real sources
    sources = [
        {
            "type": "website",
            "url": "https://news.ycombinator.com"  # Hacker News
        },
        {
            "type": "api",
            "endpoint": "https://api.github.com/repos/python/cpython",
            "headers": {"Accept": "application/vnd.github.v3+json"}
        }
    ]
    
    print("Testing with real data sources...\n")
    results = await agent.run(sources, parallel=True)
    
    # Display results
    for i, result in enumerate(results, 1):
        print(f"\n{'='*60}")
        print(f"Source {i}: {result['source']}")
        print(f"{'='*60}")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print(f"Entry ID: {result['entry_id']}")
            print(f"Quality Metrics:")
            for metric, value in result['quality_metrics'].items():
                print(f"  - {metric}: {value:.2%}")
            print(f"Entities Found: {result['metadata']['entities_found']}")
            print(f"Needs Review: {result['needs_review']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Check review queue
    reviews = agent.get_review_queue()
    if reviews:
        print(f"\n{'='*60}")
        print(f"REVIEW QUEUE: {len(reviews)} items")
        print(f"{'='*60}")
        for review in reviews:
            print(f"- Entry {review['id']}: {review['source_url']}")

if __name__ == "__main__":
    asyncio.run(test_real_sources())
```

---

## 🎯 Quick Testing Workflow

### For Development
```bash
# 1. Run demo to verify basic functionality
python demo.py

# 2. Run unit tests
pytest tests/ -v

# 3. Check code coverage
pytest tests/ --cov=. --cov-report=term-missing
```

### For CI/CD Pipeline
```bash
# In your CI/CD configuration
python -m pytest tests/ --junitxml=test-results.xml --cov=. --cov-report=xml
```

### For Pre-Deployment
```bash
# 1. Run all tests
pytest tests/ -v

# 2. Test with real data (staging environment)
python test_run.py

# 3. Verify logs
cat logs/agent.log | tail -50
```

---

## 🔍 Testing Components Individually

### Test Web Scraper
```python
from modules.collector.web_scraper import SelfHealingScraper

scraper = SelfHealingScraper()
result = scraper.scrape_with_retry("https://example.com")
print(result)
```

### Test API Client
```python
from modules.collector.api_client import RateLimitedAPIClient

client = RateLimitedAPIClient()
result = client.call_api("https://api.github.com/users/github")
print(result)
```

### Test Data Cleaner
```python
from modules.processor.data_cleaner import clean_data
import json

data = '[{"name": "JOHN", "age": "25"}, {"name": "JANE", "age": "30"}]'
cleaned = clean_data(data, "json")
print(json.loads(cleaned))
```

### Test NLP Extractor
```python
from modules.processor.nlp_extractor import extract_entities

text = "Microsoft and Google are tech companies in California."
entities = extract_entities(text)
print(entities)
```

---

## 📊 Testing Checklist

### Before Committing Code
- [ ] Run `python demo.py` - Demo works
- [ ] Run `pytest tests/` - All tests pass
- [ ] Check code coverage > 80%
- [ ] No import errors
- [ ] Logs are clean

### Before Deployment
- [ ] Demo test passes
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Real data test successful
- [ ] Review queue working
- [ ] Documentation updated
- [ ] Environment variables configured

---

## 🐛 Debugging Tests

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Run Single Test with Output
```bash
pytest tests/test_agents.py::test_collector_url_validation -v -s
```

### Use pytest Debugging
```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger immediately
pytest tests/ --pdb --pdbcls=IPython.terminal.debugger:Pdb
```

### Check Test Coverage
```bash
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 📝 Common Test Issues & Solutions

### Issue: Import Errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: No module named 'pytest'
```bash
# Solution: Install pytest
pip install pytest pytest-asyncio
```

### Issue: Tests timeout
```bash
# Solution: Increase timeout
pytest tests/ --timeout=60
```

### Issue: spaCy model not found
```bash
# Solution: Download model
python -m spacy download en_core_web_sm
```

---

## 🎓 Test Examples by Difficulty

### Beginner: Demo Test
```bash
python demo.py
```

### Intermediate: Unit Tests
```bash
pytest tests/test_agents.py -v
```

### Advanced: Custom Integration Test
```python
# Create your own test combining multiple components
import asyncio
from main import IntelligentAgent

async def my_custom_test():
    agent = IntelligentAgent()
    # Your custom testing logic
    pass

asyncio.run(my_custom_test())
```

---

## 🚀 Next Steps After Testing

1. **If demo works**: Install dependencies and try real data
2. **If tests pass**: Deploy to staging environment
3. **If tests fail**: Check logs and debug
4. **After success**: Set up CI/CD pipeline

---

## 📞 Need Help?

- **Demo issues**: Check that Python 3.9+ is installed
- **Test failures**: Check `logs/agent.log`
- **Import errors**: Run `pip install -r requirements.txt`
- **Documentation**: See `docs/project_guide.md`

---

**Remember**: Start with `python demo.py` - it's the easiest way to verify everything works! ✅