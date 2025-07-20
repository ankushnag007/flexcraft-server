from datetime import datetime
from typing import Optional

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

    id: PyObjectId = Field(default=PyObjectId(ObjectId()))
    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())
    created_by: PyObjectId = Field(...)
    updated_by: PyObjectId = Field(...)

    def model_post_init(self, __context):
        if self.__class__.__name__ in ["Register"]:
            self.created_by = PyObjectId(ObjectId("111111111111111111111111"))
            self.updated_by = PyObjectId(ObjectId("111111111111111111111111"))


class BasicFiledsUpdateDelete(BaseModel):
    """
    Base model for all schemas.
    """

    id: PyObjectId = Field(default=PyObjectId(ObjectId()))
    created_at: datetime = Field(get_current_utc_datetime())
    updated_at: datetime = Field(get_current_utc_datetime())
    created_by: PyObjectId = Field(...)
    updated_by: PyObjectId = Field(...)
