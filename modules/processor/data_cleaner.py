import pandas as pd
import numpy as np
from io import StringIO
from typing import Union, Dict, List
import json
import re

def clean_data(raw_data: Union[str, Dict, List], data_format: str = "auto") -> str:
    """
    Clean and preprocess raw data from various formats.
    
    Args:
        raw_data: Input data as string, dict, or list
        data_format: Format of input data ("auto", "csv", "json", "text")
    
    Returns:
        JSON string of cleaned data
    """
    try:
        # Convert raw data to DataFrame
        df = None
        if data_format == "auto":
            if isinstance(raw_data, (dict, list)):
                df = pd.DataFrame(raw_data)
            else:
                try:
                    df = pd.read_json(StringIO(raw_data))
                except:
                    try:
                        df = pd.read_csv(StringIO(raw_data))
                    except:
                        return clean_text(raw_data)
        elif data_format == "csv":
            df = pd.read_csv(StringIO(raw_data))
        elif data_format == "json":
            if isinstance(raw_data, str):
                df = pd.read_json(StringIO(raw_data))
            else:
                df = pd.DataFrame(raw_data)
        elif data_format == "text":
            return clean_text(raw_data)
        else:
            return json.dumps({"error": "Unsupported format"})

        if df is not None:
            # Basic cleaning
            df = df.drop_duplicates()
            
            # Handle missing values
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            
            # Fill numeric missing values with median
            for col in numeric_cols:
                df[col] = df[col].fillna(df[col].median())
            
            # Fill categorical missing values with mode
            for col in categorical_cols:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "unknown")
            
            # Clean text columns
            for col in categorical_cols:
                df[col] = df[col].astype(str).apply(clean_text)
            
            # Remove outliers from numeric columns (optional)
            # for col in numeric_cols:
            #     df = remove_outliers(df, col)
            
            return df.to_json(orient="records", indent=2)
        
        return json.dumps({"error": "Unable to process data"})
        
    except Exception as e:
        return json.dumps({"error": str(e)})

def clean_text(text: str) -> str:
    """Clean and normalize text data."""
    if not isinstance(text, str):
        return str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()

def remove_outliers(df: pd.DataFrame, column: str, n_std: float = 3) -> pd.DataFrame:
    """Remove outliers from a numeric column using standard deviation method."""
    mean = df[column].mean()
    std = df[column].std()
    df = df[(df[column] >= mean - n_std * std) & 
            (df[column] <= mean + n_std * std)]
    return df
