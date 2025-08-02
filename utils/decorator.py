import functools
import time
from typing import Union

from bson import ObjectId
from fastapi import HTTPException, Request

from constants.common import RequestMethod
from genric.authentication import decode_access_token
from schemas.auth import RegisterUpdate
from schemas.project import Project, ProjectUpdate
from utils.field_helper import project_field_helper, register_field_helper


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
        user_id = decoded_token.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="Invalid token: User ID is missing.",
            )
        company_id = decoded_token.get("company_id")
        current_time = int(time.time())
        if current_time > decoded_token["exp"]:
            raise HTTPException(status_code=401, detail="Token Expired.")
        if isinstance(request_data, Union[Project, ProjectUpdate]):
            request_data = project_field_helper(
                user_id, company_id, request_data, request_type
            )
        if isinstance(request_data, RegisterUpdate):
            request_data = register_field_helper(
                user_id, company_id, request_data, request_type
            )
        if request_type == RequestMethod.GETALL:
            if not company_id:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token: Company ID is missing.",
                )
            request_data = ObjectId(company_id)

        return await func(self, request_data, request, request_type)

    return wrapper
