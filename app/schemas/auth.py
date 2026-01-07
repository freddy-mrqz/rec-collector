from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Response model for authentication token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data extracted from JWT token."""
    user_id: int | None = None


class UserRegister(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str
