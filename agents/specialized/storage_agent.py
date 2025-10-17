from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modules.storage.database_manager import store_data

logger = logging.getLogger(__name__)
Base = declarative_base()

class ProcessedData(Base):
    __tablename__ = "processed_data"
    
    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, index=True)
    collected_at = Column(DateTime)
    processed_at = Column(DateTime)
    content_hash = Column(String, index=True)
    data = Column(JSON)
    metadata = Column(JSON)
    quality_metrics = Column(JSON)
    review_status = Column(String, default="pending")
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(String, nullable=True)

class DataStorageAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.engine = create_engine(config["database_url"])
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def store_data(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store processed data with metadata and quality metrics.
        
        Args:
            processed_data: Dictionary containing processed data and metadata
            
        Returns:
            Dictionary containing storage result and metadata
        """
        try:
            if processed_data.get("status") != "success":
                return processed_data
            
            db = self.SessionLocal()
            
            # Check if data with same hash exists
            content_hash = processed_data.get("metadata", {}).get("content_hash")
            existing_entry = None
            if content_hash:
                existing_entry = db.query(ProcessedData).filter(
                    ProcessedData.content_hash == content_hash
                ).first()
            
            if existing_entry:
                logger.info(f"Data with hash {content_hash} already exists")
                db.close()
                return {
                    "status": "skipped",
                    "reason": "duplicate_content",
                    "existing_id": existing_entry.id
                }
            
            # Prepare new entry
            new_entry = ProcessedData(
                source_url=processed_data.get("source_url"),
                collected_at=datetime.fromisoformat(processed_data.get("collected_at")),
                processed_at=datetime.fromisoformat(processed_data.get("processed_at")),
                content_hash=content_hash,
                data=processed_data.get("processed_data"),
                metadata={
                    "entities": processed_data.get("entities"),
                    "validation_results": processed_data.get("validation_results"),
                    "anomalies": processed_data.get("anomalies")
                },
                quality_metrics=processed_data.get("quality_metrics"),
                review_status="pending" if processed_data.get("needs_review") else "approved"
            )
            
            # Store the data
            db.add(new_entry)
            db.commit()
            db.refresh(new_entry)
            
            result = {
                "status": "success",
                "stored_at": datetime.now().isoformat(),
                "entry_id": new_entry.id,
                "needs_review": processed_data.get("needs_review", False)
            }
            
            logger.info(f"Successfully stored processed data with ID {new_entry.id}")
            
            db.close()
            return result
            
        except Exception as e:
            error_msg = f"Error storing data: {str(e)}"
            logger.error(error_msg)
            if 'db' in locals():
                db.close()
            return {
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_data_by_id(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve stored data by ID."""
        db = self.SessionLocal()
        try:
            entry = db.query(ProcessedData).filter(ProcessedData.id == entry_id).first()
            if not entry:
                return None
            
            return {
                "id": entry.id,
                "source_url": entry.source_url,
                "collected_at": entry.collected_at.isoformat(),
                "processed_at": entry.processed_at.isoformat(),
                "data": entry.data,
                "metadata": entry.metadata,
                "quality_metrics": entry.quality_metrics,
                "review_status": entry.review_status
            }
        finally:
            db.close()
    
    def update_review_status(self, entry_id: int, status: str, reviewer: str) -> bool:
        """Update the review status of stored data."""
        db = self.SessionLocal()
        try:
            entry = db.query(ProcessedData).filter(ProcessedData.id == entry_id).first()
            if not entry:
                return False
            
            entry.review_status = status
            entry.reviewed_at = datetime.now()
            entry.reviewed_by = reviewer
            
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating review status: {str(e)}")
            return False
        finally:
            db.close()
    
    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        """Get all entries pending review."""
        db = self.SessionLocal()
        try:
            entries = db.query(ProcessedData).filter(
                ProcessedData.review_status == "pending"
            ).all()
            
            return [{
                "id": entry.id,
                "source_url": entry.source_url,
                "collected_at": entry.collected_at.isoformat(),
                "quality_metrics": entry.quality_metrics
            } for entry in entries]
        finally:
            db.close()