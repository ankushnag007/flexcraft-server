from datetime import datetime
from typing import Optional

from pydantic import (
    Field,
    field_validator,
)

from constants.project import Priority, Status
from genric.datetime_helpers import get_current_utc_datetime
from schemas.base_model import (
    BasicFiledsUpdate,
    GenricFiledsCreate,
    PyObjectId,
)


class Project(GenricFiledsCreate):
    """
    Schema for project information.
    """

    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    priority: Priority = Field(Priority.LOW)
    status: Status = Field(Status.ACTIVE)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    owner_id: Optional[PyObjectId] = Field(None)
    company_id: Optional[PyObjectId] = Field(None)
    budget: Optional[float] = Field(None, ge=0)
    used_budget: Optional[float] = Field(None, ge=0)
    remaining_budget: Optional[float] = Field(None, ge=0)

    @field_validator("start_date")
    def validate_start_date(cls, value, values):
        if value:
            if not isinstance(value, datetime):
                raise ValueError("Start date must be a datetime.")
            if value < get_current_utc_datetime():
                raise ValueError("Start date cannot be before Present date.")
        return value

    @field_validator("end_date")
    def validate_end_date(cls, value, values):
        if value:
            if not isinstance(value, datetime):
                raise ValueError("End date must be a datetime.")
            if value < get_current_utc_datetime():
                raise ValueError("End date cannot be before Present date.")
        return value


class ProjectUpdate(BasicFiledsUpdate):
    """
    Schema for project information.
    """

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    priority: Optional[Priority] = Field(None)
    status: Optional[Status] = Field(None)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    owner_id: Optional[PyObjectId] = Field(None)
    company_id: Optional[PyObjectId] = Field(None)
    budget: Optional[float] = Field(None, ge=0)
    used_budget: Optional[float] = Field(None, ge=0)
    remaining_budget: Optional[float] = Field(None, ge=0)

    @field_validator("start_date")
    def validate_start_date(cls, value, values):
        if value:
            if not isinstance(value, datetime):
                raise ValueError("Start date must be a datetime.")
            if value < get_current_utc_datetime():
                raise ValueError("Start date cannot be before Present date.")
        return value

    @field_validator("end_date")
    def validate_end_date(cls, value, values):
        if value:
            if not isinstance(value, datetime):
                raise ValueError("End date must be a datetime.")
            if value < get_current_utc_datetime():
                raise ValueError("End date cannot be before Present date.")
        return value
