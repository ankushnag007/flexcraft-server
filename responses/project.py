import httpx
from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError, jwt
from pydantic import SecretStr
from pymongo.errors import DuplicateKeyError
from requests_oauthlib import OAuth2Session

from constants.common import DefaultRoles, ExceptionType, RequestMethod
from genric.authentication import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from genric.encrypt import PasswordCipher
from genric.serializer import custom_jsonable_encoder
from schemas.auth import (
    GoogleRegister,
    InitialRegister,
    Login,
    RefreshToken,
    Register,
    RegisterUpdate,
    ResetPassword,
)
from schemas.project import Project as project_create_dto
from services.email import send_mail_html
from utils.decorator import validate_token
from utils.generate_unique_code import generate_invite_code, generate_unique_company_id

from . import project_collection


class ProjectResponse:
    """
    Response class for project-related operations.
    """

    @validate_token
    async def create(
        self,
        project_dto: project_create_dto,
        request: Request,
        request_type: RequestMethod = RequestMethod.POST,
    ):
        try:
            project_info_dict = project_dto.model_dump()
            project_collection.insert_one(project_info_dict)
            return JSONResponse(
                status_code=201,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "Project created successfully!",
                    "data": custom_jsonable_encoder(project_info_dict),
                },
            )
        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate key error: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"An error occurred while creating the project: {str(e)}",
            )
