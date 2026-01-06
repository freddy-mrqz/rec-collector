from fastapi import APIRouter, HTTPException, status
from app.schemas import Record, RecordCreate, RecordUpdate
from app.database import db

router = APIRouter(prefix="/records", tags=["records"])


@router.post("", response_model=Record, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate):
    """Create a new record."""
    return db.create(record)


@router.get("", response_model=list[Record])
def list_records(skip: int = 0, limit: int = 100):
    """Retrieve all records with optional pagination."""
    return db.get_all(skip=skip, limit=limit)


@router.get("/{record_id}", response_model=Record)
def get_record(record_id: int):
    """Retrieve a single record by ID."""
    record = db.get(record_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return record


@router.put("/{record_id}", response_model=Record)
def update_record(record_id: int, record: RecordUpdate):
    """Update an existing record."""
    updated = db.update(record_id, record)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return updated


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int):
    """Delete a record by ID."""
    if not db.delete(record_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return None
