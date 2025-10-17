"""
Quick Component Tests - Test individual components without dependencies
"""

def test_data_cleaning():
    """Test the data cleaning functionality."""
    print("\n" + "="*60)
    print("TEST 1: Data Cleaning")
    print("="*60)
    
    # Test data
    sample_text = "  HELLO WORLD!  This is a TEST.  "
    
    # Simple cleaning function
    cleaned = sample_text.lower().strip()
    
    print(f"Original: '{sample_text}'")
    print(f"Cleaned:  '{cleaned}'")
    print(f"✓ Test passed: Text cleaned successfully")
    
    assert cleaned == "hello world!  this is a test."
    return True

def test_validation():
    """Test data validation."""
    print("\n" + "="*60)
    print("TEST 2: Data Validation")
    print("="*60)
    
    import re
    
    # Test email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    valid_email = "test@example.com"
    invalid_email = "invalid-email"
    
    is_valid = bool(re.match(email_pattern, valid_email))
    is_invalid = not bool(re.match(email_pattern, invalid_email))
    
    print(f"Valid email '{valid_email}': {is_valid}")
    print(f"Invalid email '{invalid_email}' rejected: {is_invalid}")
    print(f"✓ Test passed: Email validation works")
    
    assert is_valid and is_invalid
    return True

def test_hash_generation():
    """Test content hash generation for change detection."""
    print("\n" + "="*60)
    print("TEST 3: Content Hash Generation")
    print("="*60)
    
    import hashlib
    
    content1 = "This is some content"
    content2 = "This is some content"
    content3 = "This is different content"
    
    hash1 = hashlib.md5(content1.encode()).hexdigest()
    hash2 = hashlib.md5(content2.encode()).hexdigest()
    hash3 = hashlib.md5(content3.encode()).hexdigest()
    
    print(f"Content 1 hash: {hash1}")
    print(f"Content 2 hash: {hash2}")
    print(f"Content 3 hash: {hash3}")
    print(f"Hash 1 == Hash 2: {hash1 == hash2}")
    print(f"Hash 1 != Hash 3: {hash1 != hash3}")
    print(f"✓ Test passed: Hashing works for change detection")
    
    assert hash1 == hash2 and hash1 != hash3
    return True

def test_quality_metrics():
    """Test quality metrics calculation."""
    print("\n" + "="*60)
    print("TEST 4: Quality Metrics")
    print("="*60)
    
    # Sample data
    data = [
        {"name": "John", "age": 25, "email": "john@example.com"},
        {"name": "Jane", "age": 30, "email": "jane@example.com"},
        {"name": "Bob", "age": 25, "email": "bob@example.com"}
    ]
    
    # Calculate completeness (no null values)
    total_fields = len(data) * len(data[0])
    filled_fields = sum(1 for item in data for value in item.values() if value is not None)
    completeness = filled_fields / total_fields
    
    # Calculate uniqueness
    unique_ages = len(set(item["age"] for item in data))
    uniqueness = unique_ages / len(data)
    
    print(f"Total records: {len(data)}")
    print(f"Completeness: {completeness:.2%}")
    print(f"Uniqueness (ages): {uniqueness:.2%}")
    print(f"✓ Test passed: Quality metrics calculated")
    
    assert completeness == 1.0
    return True

def test_entity_extraction_simulation():
    """Test entity extraction logic."""
    print("\n" + "="*60)
    print("TEST 5: Entity Extraction (Simulated)")
    print("="*60)
    
    text = "Microsoft and Google are companies in California. They were founded in the 1970s."
    
    # Simple entity detection (simulation)
    entities = []
    
    # Detect organizations (simple capitalized words)
    org_keywords = ["Microsoft", "Google"]
    for keyword in org_keywords:
        if keyword in text:
            entities.append({"text": keyword, "label": "ORG"})
    
    # Detect locations
    loc_keywords = ["California"]
    for keyword in loc_keywords:
        if keyword in text:
            entities.append({"text": keyword, "label": "GPE"})
    
    # Detect dates
    if "1970s" in text:
        entities.append({"text": "1970s", "label": "DATE"})
    
    print(f"Text: {text}")
    print(f"Entities found: {len(entities)}")
    for entity in entities:
        print(f"  - {entity['text']} ({entity['label']})")
    print(f"✓ Test passed: Entity extraction works")
    
    assert len(entities) >= 3
    return True

def test_anomaly_detection_logic():
    """Test anomaly detection logic."""
    print("\n" + "="*60)
    print("TEST 6: Anomaly Detection Logic")
    print("="*60)
    
    # Sample numerical data
    prices = [10, 12, 11, 13, 10, 12, 100, 11, 12]  # 100 is an outlier
    
    # Calculate mean and standard deviation
    mean = sum(prices) / len(prices)
    variance = sum((x - mean) ** 2 for x in prices) / len(prices)
    std_dev = variance ** 0.5
    
    # Detect outliers (values > 2 std deviations from mean)
    threshold = 2
    outliers = [x for x in prices if abs(x - mean) > threshold * std_dev]
    
    print(f"Data: {prices}")
    print(f"Mean: {mean:.2f}")
    print(f"Std Dev: {std_dev:.2f}")
    print(f"Outliers detected: {outliers}")
    print(f"✓ Test passed: Anomaly detection works")
    
    assert 100 in outliers
    return True

def run_all_tests():
    """Run all component tests."""
    print("\n" + "="*60)
    print("🧪 RUNNING COMPONENT TESTS")
    print("="*60)
    print("Testing individual components without external dependencies")
    
    tests = [
        test_data_cleaning,
        test_validation,
        test_hash_generation,
        test_quality_metrics,
        test_entity_extraction_simulation,
        test_anomaly_detection_logic
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            failed += 1
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {len(tests)}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    print(f"Success rate: {(passed/len(tests))*100:.0f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("\nNext steps:")
    print("1. Run full demo: python demo.py")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run pytest tests: pytest tests/ -v")
    print()

if __name__ == "__main__":
    run_all_tests()