from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from constants.common import ExceptionType, RequestMethod
from genric.serializer import custom_jsonable_encoder
from schemas.base_model import PyObjectId
from schemas.project import Project as project_create_dto
from utils.decorator import validate_token

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
                detail=f"{str(e)}",
            )

    @validate_token
    async def update(
        self,
        project_dto: project_create_dto,
        request: Request,
        request_type: RequestMethod = RequestMethod.PUT,
    ):
        try:
            project_info_dict = project_dto.model_dump()
            updated_project = project_collection.find_one_and_update(
                {"_id": project_info_dict["record_id"]},
                {"$set": project_info_dict},
                return_document=True,
            )
            if not updated_project:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found.",
                )
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "Project updated successfully!",
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
                detail=f"{str(e)}",
            )

    @validate_token
    async def delete(
        self,
        record_id: PyObjectId,
        request: Request,
        request_type: RequestMethod = RequestMethod.DELETE,
    ):
        try:
            is_deleted = project_collection.find_one_and_delete({"_id": record_id})
            if not is_deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found.",
                )
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "Project deleted successfully!",
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"{str(e)}",
            )

    @validate_token
    async def get(
        self,
        record_id: PyObjectId,
        request: Request,
        request_type: RequestMethod = RequestMethod.GET,
    ):
        try:
            record = project_collection.find_one({"_id": record_id})
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found.",
                )
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "data": custom_jsonable_encoder(record),
                    "message": "Project fetched successfully!",
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"{str(e)}",
            )

    @validate_token
    async def get_all(
        self,
        company_id: None,
        request: Request,
        request_type: RequestMethod = RequestMethod.GETALL,
    ):
        try:
            records = project_collection.find({"company_id": company_id}).to_list(
                length=None
            )
            if not records:
                raise HTTPException(
                    status_code=404,
                    detail="Project not found.",
                )
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "data": custom_jsonable_encoder(records),
                    "message": "Project fetched all successfully!",
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"{str(e)}",
            )