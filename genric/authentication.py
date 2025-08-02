from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt

from genric.datetime_helpers import get_current_utc_datetime
from services import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = get_current_utc_datetime() + (
        expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = get_current_utc_datetime() + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, expected_type="access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise JWTError("Invalid token type")
        return payload
    except JWTError:
        return None


def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token  # This will be a dictionary
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=404,
            detail="Token has expired.",
        )
    except JWTError:
        raise HTTPException(
            status_code=404,
            detail="Invalid token.",
        )
