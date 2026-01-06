from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase

from app.schemas import RecordCreate, RecordUpdate, Record


class Base(DeclarativeBase):
    pass


class InMemoryDatabase:
    def __init__(self):
        self._records: dict[int, dict] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def create(self, record: RecordCreate) -> Record:
        record_id = self._next_id()
        now = datetime.utcnow()
        data = {
            "id": record_id,
            "title": record.title,
            "artist": record.artist,
            "discogs_id": record.discogs_id,
            "release_year": record.release_year,
            "label": record.label,
            "catalog_number": record.catalog_number,
            "media_condition": record.media_condition,
            "sleeve_condition": record.sleeve_condition,
            "notes": record.notes,
            "purchase_price": record.purchase_price,
            "purchase_date": record.purchase_date,
            "added_at": now,
            "updated_at": None,
        }
        self._records[record_id] = data
        return Record(**data)

    def get(self, record_id: int) -> Optional[Record]:
        data = self._records.get(record_id)
        if data:
            return Record(**data)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Record]:
        records = list(self._records.values())
        return [Record(**data) for data in records[skip : skip + limit]]

    def update(self, record_id: int, record: RecordUpdate) -> Optional[Record]:
        if record_id not in self._records:
            return None

        data = self._records[record_id]
        update_data = record.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            data[field] = value

        data["updated_at"] = datetime.utcnow()
        self._records[record_id] = data
        return Record(**data)

    def delete(self, record_id: int) -> bool:
        if record_id in self._records:
            del self._records[record_id]
            return True
        return False


db = InMemoryDatabase()
