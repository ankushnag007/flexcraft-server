from typing import Dict, List, Optional, Type

from bson import ObjectId
from fastapi import APIRouter, Request
from pydantic import BaseModel

from constants.common import RequestMethod


def generate_crud_routes(
    dto_create: Type[BaseModel],
    response_model,
    prefix: str,
    *,
    tags: Optional[List[str]] = None,
    include_create: bool = True,
    include_read: bool = True,
    include_read_all: bool = True,
    include_update: bool = True,
    include_delete: bool = True,
    include_in_schema: bool = True,
    dto_update: Optional[Type[BaseModel]] = None,
) -> APIRouter:
    router = APIRouter()
    crud_service = response_model()
    if not dto_update:
        dto_update = dto_create

    if include_create:

        @router.post(f"{prefix}", response_model=Dict, tags=tags, include_in_schema=include_in_schema)
        async def create_item(
            item: dto_create,
            request: Request,
            request_type: RequestMethod = RequestMethod.POST,
        ):
            return await crud_service.create(item, request, request_type)

    if include_read:

        @router.get(f"{prefix}/{{item_id}}", response_model=Dict | None, tags=tags, include_in_schema=include_in_schema)
        async def get_item(
            item_id: ObjectId,
            request: Request,
            request_type: RequestMethod = RequestMethod.GET,
        ):
            return await crud_service.read(item_id, request, request_type)

    if include_read_all:

        @router.get(f"{prefix}", response_model=List[Dict], tags=tags, include_in_schema=include_in_schema)
        async def get_all_items(
            request: Request, request_type: RequestMethod = RequestMethod.GETALL
        ):
            return await crud_service.read_all(request, request_type)

    if include_update:

        @router.put(
            f"{prefix}",
            response_model=Dict | None,
            tags=tags,
            include_in_schema=include_in_schema,
        )
        async def update_item(
            item: dto_update,
            request: Request,
            request_type: RequestMethod = RequestMethod.PUT,
        ):
            return await crud_service.update(item, request, request_type)

    if include_delete:

        @router.delete(f"{prefix}/{{item_id}}", response_model=Dict, tags=tags, include_in_schema=include_in_schema)
        async def delete_item(
            item_id: ObjectId,
            request: Request,
            request_type: RequestMethod = RequestMethod.DELETE,
        ):
            return await crud_service.delete(item_id, request, request_type)

    return router
