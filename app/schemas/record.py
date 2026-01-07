from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RecordBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    artist: str = Field(..., min_length=1, max_length=255)
    discogs_id: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1900, le=2100)
    label: Optional[str] = None
    catalog_number: Optional[str] = None
    media_condition: Optional[str] = None
    sleeve_condition: Optional[str] = None
    notes: Optional[str] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    purchase_date: Optional[datetime] = None


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    artist: Optional[str] = Field(None, min_length=1, max_length=255)
    discogs_id: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1900, le=2100)
    label: Optional[str] = None
    catalog_number: Optional[str] = None
    media_condition: Optional[str] = None
    sleeve_condition: Optional[str] = None
    notes: Optional[str] = None
    purchase_price: Optional[float] = Field(None, ge=0)
    purchase_date: Optional[datetime] = None


class Record(RecordBase):
    id: int
    user_id: Optional[int] = None
    imported_from_discogs: bool = False
    added_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
