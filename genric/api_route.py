from typing import Dict, List, Optional, Type

from bson import ObjectId
from fastapi import APIRouter
from pydantic import BaseModel


def generate_crud_routes(
    dto: Type[BaseModel],
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
) -> APIRouter:
    router = APIRouter()
    crud_service = response_model()

    if include_create:

        @router.post(f"{prefix}", response_model=Dict, tags=tags, include_in_schema=include_in_schema)
        def create_item(item: dto):
            return crud_service.create(item)

    if include_read:

        @router.get(f"{prefix}/{{item_id}}", response_model=Dict | None, tags=tags, include_in_schema=include_in_schema)
        def get_item(item_id: ObjectId):
            return crud_service.read(item_id)

    if include_read_all:

        @router.get(f"{prefix}", response_model=List[Dict], tags=tags, include_in_schema=include_in_schema)
        def get_all_items():
            return crud_service.read_all()

    if include_update:

        @router.put(f"{prefix}/{{item_id}}", response_model=Dict | None, tags=tags, include_in_schema=include_in_schema)
        def update_item(item_id: ObjectId, item: dto):
            return crud_service.update(item_id, item)

    if include_delete:

        @router.delete(f"{prefix}/{{item_id}}", response_model=Dict, tags=tags, include_in_schema=include_in_schema)
        def delete_item(item_id: ObjectId):
            return crud_service.delete(item_id)

    return router
