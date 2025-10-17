# Intelligent Agent Project - Complete Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

This intelligent agent system automates data collection, processing, and storage with built-in quality controls and adaptability.

### Key Features

- **Autonomous Data Collection**: Scrapes websites and calls APIs automatically
- **Self-Healing Scrapers**: Adapts to website layout changes
- **Data Quality Validation**: Validates data against configurable rules
- **Anomaly Detection**: Uses ML to detect unusual patterns
- **Human-in-the-Loop**: Queues problematic data for review
- **Incremental Processing**: Only processes changed data
- **Multi-Agent System**: Specialized agents work together
- **Cloud-Ready**: Deployable to Azure Functions or AWS Lambda

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  Intelligent Agent System                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Collector   │→ │  Processor   │→ │   Storage    │ │
│  │    Agent     │  │    Agent     │  │    Agent     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                  │                  │         │
│         ↓                  ↓                  ↓         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Web Scraper  │  │Data Cleaner  │  │  Database    │ │
│  │ API Client   │  │NLP Extractor │  │  Manager     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Collection**: Agent fetches data from configured sources
2. **Validation**: Checks data against validation rules
3. **Processing**: Cleans, transforms, and extracts entities
4. **Quality Check**: Calculates quality metrics and detects anomalies
5. **Review**: Queues low-quality data for human review
6. **Storage**: Saves processed data with metadata

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd intelligent_agent_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Run setup script**
   ```bash
   python setup.py
   ```

---

## Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./agent_data.db

# Optional - Email notifications
NOTIFICATION_EMAIL=alerts@yourdomain.com

# Optional - Azure deployment
AZURE_FUNCTION_APP_NAME=intelligent-agent
AZURE_RESOURCE_GROUP=agent-resources
AZURE_STORAGE_ACCOUNT=agentstorage
AZURE_LOCATION=eastus

# Optional - AWS deployment
AWS_LAMBDA_FUNCTION_NAME=intelligent-agent
AWS_REGION=us-east-1
AWS_S3_BUCKET=agent-data-bucket
```

### Configuration Files

Edit `config/settings.py` to customize:

- **Validation Rules**: Define data format and range constraints
- **Rate Limits**: Set request limits per time window
- **Quality Thresholds**: Configure auto-approval criteria
- **Review Settings**: Adjust review queue parameters

Example validation rule:
```python
PROCESSOR_CONFIG = {
    "validation_rules": {
        "email": [{
            "type": "format",
            "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        }],
        "price": [{
            "type": "range",
            "min": 0,
            "max": 1000000
        }]
    }
}
```

---

## Usage Examples

### Basic Usage

```python
import asyncio
from main import IntelligentAgent

async def main():
    # Initialize agent
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
    
    # Process sources
    results = await agent.run(sources, parallel=True)
    
    # Print results
    for result in results:
        print(f"Source: {result['source']}")
        print(f"Status: {result['status']}")
        print(f"Quality: {result['quality_metrics']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Manual Review Workflow

```python
# Get pending reviews
reviews = agent.get_review_queue()

for review in reviews:
    print(f"Entry ID: {review['id']}")
    print(f"Source: {review['source_url']}")
    print(f"Quality: {review['quality_metrics']}")
    
    # Get full data
    data = agent.get_data_by_id(review['id'])
    
    # Review and approve/reject
    if quality_check_passes(data):
        agent.approve_review(review['id'], reviewer="admin")
    else:
        agent.reject_review(review['id'], reviewer="admin", reason="Invalid data")
```

### Custom Data Source

```python
from agents.specialized.collector_agent import DataCollectorAgent
from config.settings import AGENT_CONFIG

# Initialize collector
collector = DataCollectorAgent(AGENT_CONFIG["collector"])

# Collect from custom source
result = collector.collect_data({
    "type": "api",
    "endpoint": "https://custom-api.com/data",
    "params": {"category": "tech", "limit": 100},
    "headers": {"Authorization": "Bearer YOUR_TOKEN"}
})

print(result)
```

---

## API Reference

### IntelligentAgent Class

#### Methods

- `__init__()`: Initialize the agent system
- `async process_data_source(source, review_required=True)`: Process single source
- `async run(sources, parallel=True)`: Process multiple sources
- `get_review_queue()`: Get pending review items
- `approve_review(entry_id, reviewer)`: Approve a review
- `reject_review(entry_id, reviewer, reason)`: Reject a review
- `get_data_by_id(entry_id)`: Retrieve stored data

### DataCollectorAgent Class

#### Methods

- `collect_data(source)`: Collect data from a source
- `get_collection_status(source_url)`: Check collection status

### DataProcessorAgent Class

#### Methods

- `process_data(data)`: Process and validate data
- `get_review_queue()`: Get items pending review

### DataStorageAgent Class

#### Methods

- `store_data(processed_data)`: Store processed data
- `get_data_by_id(entry_id)`: Retrieve data by ID
- `update_review_status(entry_id, status, reviewer)`: Update review status
- `get_pending_reviews()`: Get all pending reviews

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest tests/ --cov=.
```

### Test Structure

```
tests/
├── __init__.py
├── test_agents.py          # Agent tests
├── test_collector.py       # Collector tests
├── test_processor.py       # Processor tests
└── test_storage.py         # Storage tests
```

### Writing Tests

```python
import pytest
from agents.specialized.collector_agent import DataCollectorAgent

@pytest.fixture
def collector():
    return DataCollectorAgent({})

def test_url_validation(collector):
    result = collector.collect_data({
        "type": "website",
        "url": "invalid-url"
    })
    assert result["status"] == "error"
```

---

## Deployment

### Azure Functions

1. **Install Azure CLI**
   ```bash
   pip install azure-cli
   ```

2. **Login to Azure**
   ```bash
   az login
   ```

3. **Create Function App**
   ```bash
   az functionapp create --resource-group <resource-group> \
     --consumption-plan-location eastus \
     --runtime python --runtime-version 3.9 \
     --functions-version 4 \
     --name <function-app-name> \
     --storage-account <storage-account>
   ```

4. **Deploy**
   ```bash
   func azure functionapp publish <function-app-name>
   ```

### AWS Lambda

1. **Install AWS CLI**
   ```bash
   pip install awscli
   ```

2. **Configure AWS**
   ```bash
   aws configure
   ```

3. **Package application**
   ```bash
   pip install --target ./package -r requirements.txt
   cd package
   zip -r ../deployment.zip .
   cd ..
   zip -g deployment.zip main.py
   ```

4. **Deploy**
   ```bash
   aws lambda create-function --function-name intelligent-agent \
     --runtime python3.9 \
     --role <iam-role-arn> \
     --handler main.lambda_handler \
     --zip-file fileb://deployment.zip
   ```

---

## Troubleshooting

### Common Issues

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'package_name'`

**Solution**:
```bash
pip install -r requirements.txt
```

#### OpenAI API Errors

**Problem**: `openai.error.AuthenticationError`

**Solution**: Check your `.env` file and ensure `OPENAI_API_KEY` is set correctly.

#### Database Errors

**Problem**: `sqlalchemy.exc.OperationalError`

**Solution**: Ensure database directory exists and has write permissions.

#### Rate Limiting

**Problem**: Too many API requests

**Solution**: Adjust rate limits in `config/settings.py`:
```python
COLLECTOR_CONFIG = {
    "rate_limits": {
        "default": 1,  # Reduce to 1 request per second
    }
}
```

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- Check logs in `logs/agent.log`
- Review test output: `pytest tests/ -v`
- Check configuration in `config/settings.py`

---

## Best Practices

1. **Data Quality**
   - Set strict validation rules
   - Monitor quality metrics
   - Review flagged data promptly

2. **Performance**
   - Use parallel processing for multiple sources
   - Enable incremental processing
   - Optimize database queries

3. **Security**
   - Store API keys in environment variables
   - Use HTTPS for all requests
   - Validate all input data

4. **Monitoring**
   - Check logs regularly
   - Monitor review queue size
   - Track quality metrics over time

---

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub or contact the development team.
