from typing import Dict, Any, List, Union
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging
from modules.processor.data_cleaner import clean_data
from modules.processor.nlp_extractor import extract_entities
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)

class DataProcessorAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.anomaly_detector = IsolationForest(
            contamination=config.get('anomaly_threshold', 0.1),
            random_state=42
        )
        self.validation_rules = config.get('validation_rules', {})
        self.review_queue = []  # Queue for human review
        
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process collected data with validation, cleaning, and anomaly detection.
        
        Args:
            data: Dictionary containing collected data and metadata
            
        Returns:
            Dictionary containing processed data and quality metrics
        """
        try:
            if data.get("status") != "success":
                return data
            
            content = data.get("content")
            source_type = data.get("source_type")
            
            # Clean and structure the data
            cleaned_data = clean_data(content, data_format="auto")
            
            # Convert to DataFrame for analysis
            if isinstance(cleaned_data, str):
                try:
                    df = pd.read_json(cleaned_data)
                except:
                    df = pd.DataFrame({"content": [cleaned_data]})
            else:
                df = pd.DataFrame(cleaned_data)
            
            # Extract entities
            entities = json.loads(extract_entities(content))
            
            # Perform data validation
            validation_results = self._validate_data(df)
            
            # Detect anomalies in numerical columns
            anomalies = self._detect_anomalies(df)
            
            # Calculate data quality metrics
            quality_metrics = self._calculate_quality_metrics(df)
            
            # Determine if human review is needed
            needs_review = (
                len(validation_results["failures"]) > 0 or 
                anomalies["anomaly_score"] > self.config.get("review_threshold", 0.5)
            )
            
            if needs_review:
                self._queue_for_review(data, validation_results, anomalies)
            
            result = {
                "status": "success",
                "source_url": data.get("source_url"),
                "processed_at": datetime.now().isoformat(),
                "processed_data": json.loads(cleaned_data) if isinstance(cleaned_data, str) else cleaned_data,
                "entities": entities,
                "quality_metrics": quality_metrics,
                "validation_results": validation_results,
                "anomalies": anomalies,
                "needs_review": needs_review
            }
            
            logger.info(f"Successfully processed data from {data.get('source_url')}")
            return result
            
        except Exception as e:
            error_msg = f"Error processing data: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def _validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Apply validation rules to the data."""
        failures = []
        warnings = []
        
        for column, rules in self.validation_rules.items():
            if column not in df.columns:
                warnings.append(f"Column {column} not found in data")
                continue
                
            for rule in rules:
                rule_type = rule.get("type")
                if rule_type == "range":
                    min_val, max_val = rule.get("min"), rule.get("max")
                    mask = ~df[column].between(min_val, max_val)
                    if mask.any():
                        failures.append({
                            "column": column,
                            "rule": "range",
                            "values": df.loc[mask, column].tolist()
                        })
                
                elif rule_type == "format":
                    pattern = rule.get("pattern")
                    mask = ~df[column].astype(str).str.match(pattern)
                    if mask.any():
                        failures.append({
                            "column": column,
                            "rule": "format",
                            "values": df.loc[mask, column].tolist()
                        })
        
        return {
            "failures": failures,
            "warnings": warnings
        }
    
    def _detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies in numerical data."""
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) == 0:
            return {"anomaly_score": 0, "anomalies": []}
        
        # Fit and predict anomalies
        numerical_data = df[numerical_cols].fillna(df[numerical_cols].mean())
        predictions = self.anomaly_detector.fit_predict(numerical_data)
        
        # Calculate anomaly score and identify anomalous rows
        anomaly_score = (predictions == -1).mean()
        anomalous_rows = df.index[predictions == -1].tolist()
        
        return {
            "anomaly_score": float(anomaly_score),
            "anomalous_rows": anomalous_rows
        }
    
    def _calculate_quality_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate various data quality metrics."""
        return {
            "completeness": 1 - df.isnull().mean().mean(),
            "uniqueness": df.nunique().mean() / len(df),
            "consistency": self._check_consistency(df)
        }
    
    def _check_consistency(self, df: pd.DataFrame) -> float:
        """Check data consistency across columns."""
        consistency_score = 1.0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            # Check for correlation consistency
            corr_matrix = df[numeric_cols].corr()
            consistency_score = abs(corr_matrix).mean().mean()
        
        return float(consistency_score)
    
    def _queue_for_review(self, data: Dict[str, Any], validation_results: Dict[str, Any], anomalies: Dict[str, Any]):
        """Queue data for human review."""
        self.review_queue.append({
            "timestamp": datetime.now().isoformat(),
            "source_url": data.get("source_url"),
            "validation_failures": validation_results["failures"],
            "anomaly_score": anomalies["anomaly_score"],
            "status": "pending_review"
        })
    
    def get_review_queue(self) -> List[Dict[str, Any]]:
        """Get the current review queue."""
        return self.review_queue