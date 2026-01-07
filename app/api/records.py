from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import Record, RecordCreate, RecordUpdate
from app.database import get_db
from app.models.record import Record as RecordModel
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/records", tags=["records"])


@router.post("", response_model=Record, status_code=status.HTTP_201_CREATED)
def create_record(
    record: RecordCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new record for the authenticated user."""
    db_record = RecordModel(
        **record.model_dump(),
        user_id=current_user.id,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("", response_model=list[Record])
def list_records(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve all records for the authenticated user."""
    records = (
        db.query(RecordModel)
        .filter(RecordModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records


@router.get("/{record_id}", response_model=Record)
def get_record(
    record_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Retrieve a single record by ID."""
    record = (
        db.query(RecordModel)
        .filter(RecordModel.id == record_id, RecordModel.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return record


@router.put("/{record_id}", response_model=Record)
def update_record(
    record_id: int,
    record: RecordUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update an existing record."""
    db_record = (
        db.query(RecordModel)
        .filter(RecordModel.id == record_id, RecordModel.user_id == current_user.id)
        .first()
    )
    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete a record by ID."""
    db_record = (
        db.query(RecordModel)
        .filter(RecordModel.id == record_id, RecordModel.user_id == current_user.id)
        .first()
    )
    if db_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )

    db.delete(db_record)
    db.commit()
    return None
