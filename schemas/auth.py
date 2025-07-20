import re
from datetime import datetime, timedelta, tzinfo
from typing import Annotated, Dict, Literal, Optional

from bson import ObjectId
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    StringConstraints,
    field_validator,
)

from constants.common import DefaultRoles
from genric.datetime_helpers import get_current_utc_datetime
from schemas.base_model import BasicFiledsCreate


class Company(BaseModel):
    """
    Schema for company information.
    """

    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=255)
    phone_number: Annotated[str, StringConstraints(pattern=r"^\d{10}$")] = Field(
        ..., min_length=10, max_length=10
    )
    sec_phone_number: Optional[
        Annotated[str, StringConstraints(pattern=r"^\d{10}$")]
    ] = Field(..., min_length=10, max_length=10)
    domain: str = Field(...)
    invite_code: Optional[str] = Field(...)
    image: Optional[str] = Field(None)
    bck_image: Optional[str] = Field(None)
    email: EmailStr = Field(..., min_length=5, max_length=128)
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    timezone: Optional[str] = Field(None, min_length=2, max_length=50)
    country_code: Optional[str] = Field(None, min_length=2, max_length=10)


class Register(BasicFiledsCreate):
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password:SecretStr = Field(..., min_length=6, max_length=25)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    role: DefaultRoles = Field(DefaultRoles.USER)
    is_google_login: bool = False
    is_verified: bool = False
    phone_number: Annotated[str, StringConstraints(pattern=r"^\d{10}$")] = Field(
        ..., min_length=10, max_length=10
    )
    image: Optional[str] = Field(None)
    bck_image: Optional[str] = Field(None)
    country: Optional[str] = Field(...)
    timezone: Optional[str] = Field(None, min_length=2, max_length=50)
    country_code: Optional[str] = Field(None, min_length=2, max_length=10)
    is_two_factor_auth: bool = Field(False)
    last_login: Optional[datetime] = Field(get_current_utc_datetime())

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
        validate_by_name = True
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


class ResetPassword(BaseModel):
    """
    Schema for Reset password request.
    """

    email: EmailStr = Field(..., min_length=5, max_length=128)
    old_password: SecretStr = Field(..., min_length=6, max_length=25)
    new_password: SecretStr = Field(..., min_length=6, max_length=25)
    confirm_password: SecretStr = Field(..., min_length=6, max_length=25)

    @field_validator("new_password")
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


class GoogleOauth:
    """
    Schema for Google OAuth request.
    """

    ...


class GoogleOauthCallback(BaseModel):
    """
    Schema for Google OAuth response.
    """

    ...


class GoogleRegister(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password: None = Field(None)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    role: Literal["user", "admin"] = Field("user")
    picture: Optional[str] = Field(None)
    is_google_login: bool = Field(True)
    is_verified: bool = Field(True)
    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())