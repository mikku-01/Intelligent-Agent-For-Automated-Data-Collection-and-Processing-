# Intelligent Agent for Automated Data Collection & Processing

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered agent system for autonomous data collection, processing, and storage using modern AI/ML tools and frameworks.

## 🚀 Quick Start

### Option 1: Run Demo (No API Keys Required)

```bash
# Clone and navigate to project
cd intelligent_agent_project

# Run the demo with mock data
python demo.py
```

### Option 2: Full Setup

```bash
# 1. Run setup script
python setup.py

# 2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Configure environment
copy .env.example .env
# Edit .env with your API keys

# 4. Run tests
pytest tests/ -v

# 5. Run the agent
python test_run.py
```

## ✨ Features

- 🤖 **Autonomous Data Collection** - Scrapes websites and calls APIs automatically
- 🔄 **Self-Healing Scrapers** - Adapts to website layout changes
- ✅ **Data Quality Validation** - Validates data against configurable rules
- 🔍 **Anomaly Detection** - Uses ML to detect unusual patterns in data
- 👥 **Human-in-the-Loop** - Queues problematic data for review
- 📊 **Quality Metrics** - Tracks completeness, uniqueness, and consistency
- � **Incremental Processing** - Only processes changed data
- 🤝 **Multi-Agent System** - Specialized agents collaborate effectively
- ☁️ **Cloud-Ready** - Deployable to Azure Functions or AWS Lambda
- 📈 **Rate Limiting** - Intelligent request throttling

## � Project Structure

```
intelligent_agent_project/
├── agents/                    # Agent implementations
│   ├── core_agent.py         # Main agent orchestration
│   └── specialized/          # Specialized agent modules
│       ├── collector_agent.py
│       ├── processor_agent.py
│       └── storage_agent.py
├── modules/                   # Core functionality modules
│   ├── collector/            # Data collection
│   │   ├── web_scraper.py   # Self-healing web scraper
│   │   └── api_client.py    # Rate-limited API client
│   ├── processor/            # Data processing
│   │   ├── data_cleaner.py  # Data cleaning & transformation
│   │   └── nlp_extractor.py # NLP entity extraction
│   └── storage/              # Data persistence
│       └── database_manager.py
├── config/                   # Configuration files
│   └── settings.py          # Project settings
├── tests/                    # Test suite
│   ├── test_agents.py
│   ├── test_collector.py
│   ├── test_processor.py
│   └── test_storage.py
├── docs/                     # Documentation
│   └── project_guide.md     # Complete guide
├── logs/                     # Application logs
├── data/                     # Data storage
│   ├── raw/                 # Raw collected data
│   └── processed/           # Processed data
├── main.py                   # Main application entry
├── demo.py                   # Demo with mock data
├── test_run.py              # Test runner
├── setup.py                 # Setup script
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## 🎯 Architecture

The project is organized into several key modules:

- **Agents**: Core agent implementation using LangChain, CrewAI, and AutoGen
- **Modules**:
  - Collector: Web scraping and API integration
  - Processor: Data cleaning and NLP processing
  - Storage: Database management and persistence
- **Config**: Configuration management and settings
- **Tests**: Comprehensive test suite

### Data Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Collector  │ --> │  Processor   │ --> │   Storage   │
│    Agent    │     │    Agent     │     │    Agent    │
└─────────────┘     └──────────────┘     └─────────────┘
      │                    │                     │
      ↓                    ↓                     ↓
 Web Scraping        Data Cleaning         Database
 API Calls           Validation            Review Queue
 Rate Limiting       Anomaly Detection     Deduplication
```

## 📚 Prerequisites

- Python 3.9+
- OpenAI API key (for full functionality)
- SQLite (default) or other SQL database
- Required Python packages (see `requirements.txt`)

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./agent_data.db

# Optional
NOTIFICATION_EMAIL=alerts@example.com

# Cloud Deployment (Optional)
AZURE_FUNCTION_APP_NAME=intelligent-agent
AWS_LAMBDA_FUNCTION_NAME=intelligent-agent
```

### Validation Rules

Edit `config/settings.py` to customize validation:

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

## 💡 Usage Examples

### Basic Usage

```python
import asyncio
from main import IntelligentAgent

async def main():
    agent = IntelligentAgent()
    
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
    
    results = await agent.run(sources, parallel=True)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

### Review Workflow

```python
# Get pending reviews
reviews = agent.get_review_queue()

# Review and approve/reject
for review in reviews:
    data = agent.get_data_by_id(review['id'])
    if is_valid(data):
        agent.approve_review(review['id'], reviewer="admin")
    else:
        agent.reject_review(review['id'], reviewer="admin", reason="Invalid")
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.

# Run specific test
pytest tests/test_agents.py -v
```

## 🚢 Cloud Deployment

### Azure Functions

```bash
az login
az functionapp create --resource-group <group> \
  --consumption-plan-location eastus \
  --runtime python --runtime-version 3.9 \
  --name <app-name>
func azure functionapp publish <app-name>
```

### AWS Lambda

```bash
aws configure
pip install --target ./package -r requirements.txt
cd package && zip -r ../deployment.zip . && cd ..
zip -g deployment.zip main.py
aws lambda create-function --function-name intelligent-agent \
  --runtime python3.9 --handler main.lambda_handler \
  --zip-file fileb://deployment.zip
```

## 📖 Documentation

- [Complete Project Guide](docs/project_guide.md) - Comprehensive documentation
- [API Reference](docs/project_guide.md#api-reference) - Detailed API docs
- [Deployment Guide](docs/project_guide.md#deployment) - Cloud deployment instructions

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Run `pip install -r requirements.txt`
2. **API Errors**: Check your `.env` file and API key
3. **Database Errors**: Ensure write permissions for database directory
4. **Rate Limiting**: Adjust rate limits in `config/settings.py`

See the [Troubleshooting Guide](docs/project_guide.md#troubleshooting) for more help.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain community
- CrewAI and AutoGen frameworks
- spaCy for NLP capabilities

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](docs/project_guide.md)
- Review logs in `logs/agent.log`

---

**Built with ❤️ for autonomous data processing**
