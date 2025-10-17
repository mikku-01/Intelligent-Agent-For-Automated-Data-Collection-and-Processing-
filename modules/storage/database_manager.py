from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class CollectedData(Base):
    __tablename__ = "collected_data"
    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String)
    collected_at = Column(DateTime, default=datetime.now)
    processed_content = Column(Text)

Base.metadata.create_all(bind=engine)

def store_data(data_json: str) -> str:
    try:
        data = json.loads(data_json)
        db = SessionLocal()
        new_entry = CollectedData(
            source_url=data.get("source_url"),
            processed_content=data.get("processed_content")
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        db.close()
        return f"Data stored with ID: {new_entry.id}"
    except Exception as e:
        return f"Error: {e}"
