from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Record(Base):
    __tablename__ = "records"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Owner relationship
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    owner = relationship("User", back_populates="records")

    # External API reference (from Discogs)
    discogs_id = Column(String, index=True, nullable=True)
    imported_from_discogs = Column(Boolean, default=False)

    # Basic record information
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    label = Column(String, nullable=True)
    catalog_number = Column(String, nullable=True)
    genre = Column(String, nullable=True)

    # Collection-specific fields
    media_condition = Column(String, nullable=True)  # e.g., "Mint", "Very Good", etc.
    sleeve_condition = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    purchase_price = Column(Float, nullable=True)
    purchase_date = Column(DateTime, nullable=True)

    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Composite unique constraint - same discogs_id can exist for different users
    __table_args__ = (
        UniqueConstraint("user_id", "discogs_id", name="uq_user_discogs_id"),
    )

    def __repr__(self) -> str:
        return f"<Record(id={self.id}, title='{self.title}', artist='{self.artist}')>"
