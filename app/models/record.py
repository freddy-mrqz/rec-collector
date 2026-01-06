from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class Record(Base):
    __tablename__ = "records"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # External API reference (from Discogs or whatever we use)
    discogs_id = Column(String, unique=True, index=True, nullable=True)
    
    # Basic record information
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    label = Column(String, nullable=True)
    catalog_number = Column(String, nullable=True)
    
    # Collection-specific fields
    media_condition = Column(String, nullable=True)  # e.g., "Mint", "Very Good", etc.
    sleeve_condition = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    purchase_price = Column(Float, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())