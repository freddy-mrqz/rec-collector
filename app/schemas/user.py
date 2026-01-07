from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Schema for creating a user (internal use)."""
    hashed_password: str


class User(UserBase):
    """Schema for user responses."""
    id: int
    is_active: bool
    discogs_username: str | None = None
    discogs_connected: bool = False
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserInDB(User):
    """Schema for user with hashed password (internal use)."""
    hashed_password: str
