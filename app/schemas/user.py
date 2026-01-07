from datetime import datetime
from pydantic import BaseModel, EmailStr, computed_field


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
    discogs_connected_at: datetime | None = None
    last_discogs_sync: datetime | None = None
    created_at: datetime
    updated_at: datetime | None = None

    @computed_field
    @property
    def discogs_connected(self) -> bool:
        return self.discogs_connected_at is not None

    model_config = {"from_attributes": True}


class UserInDB(User):
    """Schema for user with hashed password (internal use)."""
    hashed_password: str
