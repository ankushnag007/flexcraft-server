from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from zstd_asgi import ZstdMiddleware

from genric.api_route import generate_crud_routes
from responses.auth import GoogleOauthCallbackResponse, GoogleOauthResponse, LoginResponse, RefreshTokenResponse, RegisterResponse, ResetPasswordResponse
from schemas.auth import GoogleOauth, GoogleOauthCallback, Login, RefreshToken, Register, ResetPassword

#
# App
#
app = FastAPI(
    docs_url="/docs",
    swagger_ui_init_oauth={
        "appName": "Credentialing API",
        "usePkceWithAuthorizationCodeGrant": True,
    },
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
        dto=Register,
        response_model=RegisterResponse,
        prefix="/register",
        tags=["Auth"],
        include_read=False,
        include_read_all=False,
        include_update=False,
        include_delete=False,
    )
)

app.include_router(
    generate_crud_routes(
        dto=Login,
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
        dto=RefreshToken,
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
        dto=ResetPassword,
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
        dto=GoogleOauth,
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
        dto=GoogleOauthCallback,
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