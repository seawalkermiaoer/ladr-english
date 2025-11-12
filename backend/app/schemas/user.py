from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user model."""
    pass


class UserCreate(BaseModel):
    """Model for creating a user."""
    id: str
    # Add other user fields as needed


class UserOut(UserBase):
    """Model for user output."""
    id: str
    created_at: Optional[str] = None
    current_level: Optional[str] = None

    class Config:
        from_attributes = True


class TokenVerificationOut(BaseModel):
    """Model for token verification output."""
    ok: bool
    token: str
    user: Optional[UserOut] = None