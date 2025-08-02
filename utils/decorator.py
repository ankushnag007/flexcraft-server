import functools
import time
from functools import wraps
from inspect import iscoroutinefunction

from bson import ObjectId
from fastapi import HTTPException, Request
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    field_validator,
    model_validator,
)

from constants.common import RequestMethod
from genric.authentication import decode_access_token
from schemas.auth import Register
from schemas.project import Project as project_create_dto


def validate_token(func):
    @functools.wraps(func)
    async def wrapper(
        self, request_data, request: Request, request_type: RequestMethod
    ):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=401, detail="Authorization token is missing."
            )
        token = token.split(" ")[1] if " " in token else token
        decoded_token = decode_access_token(token)
        user_id = decoded_token["user_id"]
        company_id = decoded_token.get("company_id")
        current_time = int(time.time())
        if current_time > decoded_token["exp"]:
            raise HTTPException(status_code=401, detail="Token Expired.")
        if isinstance(request_data, project_create_dto):
            if not company_id:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token: Company ID is missing.",
                )
            if request_type == RequestMethod.POST:
                request_data.created_by = ObjectId(user_id)
                request_data.updated_by = ObjectId(user_id)
                request_data.company_id = ObjectId(company_id)
                request_data.owner_id = ObjectId(user_id)
            if request_type == RequestMethod.PUT:
                request_data.updated_by = ObjectId(user_id)
                request_data.company_id = ObjectId(company_id)

        return await func(self, request_data, request, request_type)

    return wrapper
