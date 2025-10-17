import pytest
from agents.specialized.collector_agent import DataCollectorAgent
from agents.specialized.processor_agent import DataProcessorAgent
from agents.specialized.storage_agent import DataStorageAgent
from config.settings import AGENT_CONFIG
import json

@pytest.fixture
def collector_agent():
    return DataCollectorAgent(AGENT_CONFIG["collector"])

@pytest.fixture
def processor_agent():
    return DataProcessorAgent(AGENT_CONFIG["processor"])

@pytest.fixture
def storage_agent():
    return DataStorageAgent(AGENT_CONFIG["storage"])

def test_collector_url_validation(collector_agent):
    # Test invalid URL
    invalid_source = {"type": "website", "url": "not-a-valid-url"}
    result = collector_agent.collect_data(invalid_source)
    assert result["status"] == "error"
    assert "Invalid URL" in result["error"]

    # Test valid URL
    valid_source = {"type": "website", "url": "https://example.com"}
    result = collector_agent.collect_data(valid_source)
    assert result["status"] in ["success", "error"]  # Could be error if site is down

def test_processor_data_cleaning(processor_agent):
    # Test with sample data
    sample_data = {
        "status": "success",
        "content": json.dumps([
            {"name": "John DOE", "age": "25", "email": "john.doe@example.com"},
            {"name": "Jane DOE", "age": "30", "email": "invalid-email"}
        ])
    }
    
    result = processor_agent.process_data(sample_data)
    assert result["status"] == "success"
    assert "quality_metrics" in result
    assert "validation_results" in result

def test_storage_operations(storage_agent):
    # Test storing and retrieving data
    test_data = {
        "status": "success",
        "source_url": "https://example.com",
        "processed_data": [{"test": "data"}],
        "collected_at": "2025-10-13T12:00:00",
        "processed_at": "2025-10-13T12:01:00",
        "quality_metrics": {"completeness": 1.0},
        "metadata": {"content_hash": "test_hash"}
    }
    
    store_result = storage_agent.store_data(test_data)
    assert store_result["status"] == "success"
    assert "entry_id" in store_result
    
    # Test retrieval
    entry_id = store_result["entry_id"]
    retrieved_data = storage_agent.get_data_by_id(entry_id)
    assert retrieved_data is not None
    assert retrieved_data["source_url"] == "https://example.com"

def test_end_to_end_processing(collector_agent, processor_agent, storage_agent):
    # Test the entire pipeline
    source = {"type": "website", "url": "https://example.com"}
    
    # Collection
    collection_result = collector_agent.collect_data(source)
    assert "status" in collection_result
    
    if collection_result["status"] == "success":
        # Processing
        processing_result = processor_agent.process_data(collection_result)
        assert "status" in processing_result
        
        if processing_result["status"] == "success":
            # Storage
            storage_result = storage_agent.store_data(processing_result)
            assert "status" in storage_result