from bson import ObjectId
from fastapi.encoders import jsonable_encoder


def custom_jsonable_encoder(obj):
    return jsonable_encoder(
        obj,
        custom_encoder={ObjectId: str},  # Convert ObjectId to a string
    )