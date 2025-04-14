import re
from datetime import datetime, timedelta, tzinfo
from typing import Annotated, Dict, Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, SecretStr, StringConstraints, field_validator

from genric.datetime_helpers import get_current_utc_datetime


class Register(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password:SecretStr = Field(..., min_length=6, max_length=25)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    role: Literal["user", "admin"] = Field("user")
    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())

    @field_validator("password")
    def validate_password(cls, value):
        value = value.get_secret_value()
        if len(value) < 6:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("Password must contain at least one special character (@$!%*?&).")
        return SecretStr(value)

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
        }
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Login(BaseModel):
    """
    Schema for login request.
    """
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password: SecretStr = Field(..., min_length=6, max_length=25)

class RefreshToken(BaseModel):
    """
    Schema for refresh token request.
    """
    refresh_token: str