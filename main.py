from typing import Union

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from zstd_asgi import ZstdMiddleware

from genric.api_route import generate_crud_routes
from responses.auth import (
    GoogleOauthCallbackResponse,
    GoogleOauthResponse,
    InitRegisterResponse,
    LoginResponse,
    RefreshTokenResponse,
    RegisterResponse,
    ResetPasswordResponse,
)
from responses.project import ProjectResponse
from schemas.auth import (
    GoogleOauth,
    GoogleOauthCallback,
    InitialRegister,
    Login,
    RefreshToken,
    Register,
    RegisterUpdate,
    ResetPassword,
)
from schemas.project import Project

#
# App
#
app = FastAPI(
    docs_url="/docs",
    swagger_ui_init_oauth={
        "appName": "Credentialing API",
        "usePkceWithAuthorizationCodeGrant": True,
        "authFlowType": "authorizationCode",
        "persistAuthorization": True,
    },
    title="Flexcraft API",
    description="Flexcraft API with Bearer Token",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Authentication and Authorization related endpoints.",
        },
        {
            "name": "Project",
            "description": "Project management related endpoints.",
        },
    ],
    openapi_url="/openapi.json",
    redoc_url="/redoc",  # Redoc documentation URL
    openapi_prefix="/api/v1",  # Prefix for OpenAPI schema
)

origins = [
    "*"
    # "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    ZstdMiddleware,
    minimum_size=500,
    write_checksum=True,
    write_content_size=True,
    gzip_fallback=True,
)


app.include_router(
    generate_crud_routes(
        dto_create=InitialRegister,
        response_model=InitRegisterResponse,
        prefix="/init_register",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=Register,
        dto_update=RegisterUpdate,
        response_model=RegisterResponse,
        prefix="/register",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=Login,
        response_model=LoginResponse,
        prefix="/login",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=RefreshToken,
        response_model=RefreshTokenResponse,
        prefix="/refresh-token",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=ResetPassword,
        response_model=ResetPasswordResponse,
        prefix="/reset-password",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=GoogleOauth,
        response_model=GoogleOauthResponse,
        prefix="/google-oauth",
        tags=["Auth"],
        include_create=False,
        include_read=False,
        include_read_all=True,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=GoogleOauthCallback,
        response_model=GoogleOauthCallbackResponse,
        prefix="/google-oauth-callback",
        tags=["Auth"],
        include_create=False,
        include_read=False,
        include_read_all=True,
        include_update=False,
        include_delete=False,
        include_in_schema=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto_create=Project,
        response_model=ProjectResponse,
        prefix="/projects",
        tags=["Project"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)