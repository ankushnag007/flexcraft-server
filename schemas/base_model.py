from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
)
from pydantic_core import core_schema

from genric.datetime_helpers import get_current_utc_datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class BasicFiledsCreate(BaseModel):
    """
    Base model for all schemas.
    """

    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())
    created_by: PyObjectId = Field(PyObjectId("111111111111111111111111"))
    updated_by: PyObjectId = Field(PyObjectId("111111111111111111111111"))

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
        }
        validate_by_name = True
        arbitrary_types_allowed = True


class BasicFiledsUpdate(BaseModel):
    """
    Base model for all schemas.
    """

    record_id: PyObjectId = Field(default=PyObjectId(ObjectId()))
    updated_at: datetime = Field(get_current_utc_datetime())
    updated_by: PyObjectId = Field(...)

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
        }
        validate_by_name = True
        arbitrary_types_allowed = True

class GenricFiledsCreate(BaseModel):
    """
    Base model for all schemas.
    """

    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())
    created_by: PyObjectId = Field(...)
    updated_by: PyObjectId = Field(...)

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
        }
        validate_by_name = True
        arbitrary_types_allowed = True
