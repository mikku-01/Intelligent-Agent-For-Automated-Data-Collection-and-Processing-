import os
from dotenv import load_dotenv

load_dotenv()

# Base configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agent_data.db")

# Data Collection Configuration
COLLECTOR_CONFIG = {
    "rate_limits": {
        "default": 1,  # requests per second
        "api.example.com": 5  # custom rate limit for specific domain
    },
    "retry_config": {
        "max_retries": 3,
        "backoff_factor": 2
    },
    "headers": {
        "User-Agent": "IntelligentAgent/1.0"
    }
}

# Data Processing Configuration
PROCESSOR_CONFIG = {
    "validation_rules": {
        "email": [{
            "type": "format",
            "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        }],
        "age": [{
            "type": "range",
            "min": 0,
            "max": 120
        }],
        "price": [{
            "type": "range",
            "min": 0,
            "max": 1000000
        }]
    },
    "anomaly_threshold": 0.1,
    "review_threshold": 0.5,
    "nlp_config": {
        "model": "en_core_web_sm",
        "entity_types": ["PERSON", "ORG", "GPE", "DATE"]
    }
}

# Storage Configuration
STORAGE_CONFIG = {
    "database_url": DATABASE_URL,
    "chunk_size": 1000,  # records per batch
    "archive_after_days": 30,
    "compression": True
}

# Agent System Configuration
AGENT_CONFIG = {
    "collector": COLLECTOR_CONFIG,
    "processor": PROCESSOR_CONFIG,
    "storage": STORAGE_CONFIG,
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/agent.log"
    }
}

# API endpoints configuration
API_ENDPOINTS = {
    "example_api": "https://api.example.com/data",
    "weather_api": "https://api.weather.com/v1/current",
    "news_api": "https://api.news.org/v2/top-headlines"
}

# Human review configuration
REVIEW_CONFIG = {
    "auto_approve_threshold": 0.8,  # Quality score threshold for automatic approval
    "max_queue_size": 1000,  # Maximum size of review queue
    "notification_email": os.getenv("NOTIFICATION_EMAIL"),
    "review_expiration_hours": 48  # Time before review request expires
}

# Cloud deployment configuration
CLOUD_CONFIG = {
    "azure": {
        "function_app_name": os.getenv("AZURE_FUNCTION_APP_NAME"),
        "resource_group": os.getenv("AZURE_RESOURCE_GROUP"),
        "storage_account": os.getenv("AZURE_STORAGE_ACCOUNT"),
        "location": os.getenv("AZURE_LOCATION", "eastus")
    },
    "aws": {
        "lambda_function_name": os.getenv("AWS_LAMBDA_FUNCTION_NAME"),
        "region": os.getenv("AWS_REGION", "us-east-1"),
        "s3_bucket": os.getenv("AWS_S3_BUCKET")
    }
}
