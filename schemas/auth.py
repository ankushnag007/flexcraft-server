import re
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    StringConstraints,
    field_validator,
)

from constants.common import Country, CountryCode, CountryTimezone, DefaultRoles
from schemas.base_model import (
    BasicFiledsCreate,
    BasicFiledsUpdate,
    GenricFiledsCreate,
    PyObjectId,
)


class InitialUser(BasicFiledsCreate):
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password: SecretStr = Field(..., min_length=6, max_length=25)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    role: DefaultRoles = Field(DefaultRoles.SUPER_ADMIN)

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
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)."
            )
        return SecretStr(value)

from slugify import slugify


class Company(GenricFiledsCreate):
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
    ] = Field(None, min_length=10, max_length=10)
    domain: str = Field(...)
    image: Optional[str] = Field(None)
    bck_image: Optional[str] = Field(None)
    email: EmailStr = Field(..., min_length=5, max_length=128)
    country: Country = Field(Country.INDIA)
    timezone: CountryTimezone = Field(CountryTimezone.INDIA)
    country_code: CountryCode = Field(CountryCode.INDIA)

class CompanyUpdate(BasicFiledsUpdate):
    """
    Schema for company information.
    """

    domain: Optional[str | None] = Field(None)
    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=255)
    phone_number: Annotated[str, StringConstraints(pattern=r"^\d{10}$")] = Field(
        ..., min_length=10, max_length=10
    )
    sec_phone_number: Optional[
        Annotated[str, StringConstraints(pattern=r"^\d{10}$")]
    ] = Field(None, min_length=10, max_length=10)
    image: Optional[str] = Field(None)
    bck_image: Optional[str] = Field(None)
    email: EmailStr = Field(..., min_length=5, max_length=128)
    country: Country = Field(Country.INDIA)
    timezone: CountryTimezone = Field(CountryTimezone.INDIA)
    country_code: CountryCode = Field(CountryCode.INDIA)


class User(BasicFiledsUpdate):
    email: Optional[EmailStr] = Field(..., min_length=5, max_length=128)
    password: Optional[SecretStr] = Field(..., min_length=6, max_length=25)
    first_name: Optional[str] = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    company_id: Optional[PyObjectId] = Field(None)
    role: Optional[DefaultRoles] = Field(DefaultRoles.USER)
    is_google_login: bool = False
    is_verified: bool = False
    phone_number: Annotated[str, StringConstraints(pattern=r"^\d{10}$")] = Field(
        ..., min_length=10, max_length=10
    )
    image: Optional[str] = Field(None)
    bck_image: Optional[str] = Field(None)
    country: Country = Field(Country.INDIA)
    timezone: CountryTimezone = Field(CountryTimezone.INDIA)
    country_code: CountryCode = Field(CountryCode.INDIA)
    is_two_factor_auth: Optional[bool] = Field(False)

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

class InitialRegister(BaseModel):
    """
    Schema for initial user registration.
    """

    user_details: InitialUser = Field(...)

    @field_validator("user_details")
    def validate_user_details(cls, value):
        if not value.email or not value.password:
            raise ValueError("Email and password are required.")
        return value


class Register(BaseModel):
    """
    Schema for user registration.
    """

    user_details: User = Field(...)
    company_details: Company = Field(...)

class RegisterUpdate(BaseModel):
    """
    Schema for user registration.
    """

    user_details: User = Field(...)
    company_details: CompanyUpdate = Field(...)


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


class GoogleRegister(BasicFiledsCreate):
    email: EmailStr = Field(..., min_length=5, max_length=128)
    password: None = Field(None)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    role: DefaultRoles = Field(...)
    picture: Optional[str] = Field(None)
    is_google_login: bool = Field(True)
    is_verified: bool = Field(True)