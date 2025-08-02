import functools
from functools import wraps
from inspect import iscoroutinefunction

from bson import ObjectId
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    field_validator,
    model_validator,
)


def cr_up_field_validator(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        default_id = ObjectId("111111111111111111111111")

        # Search for a Register instance in args/kwargs
        for arg in list(args) + list(kwargs.values()):
            if arg.__class__.__name__ == "Register":
                if getattr(arg, "created_by", None) is None:
                    setattr(arg, "created_by", default_id)
                if getattr(arg, "updated_by", None) is None:
                    setattr(arg, "updated_by", default_id)

        return await func(self, *args, **kwargs)

    return wrapper
