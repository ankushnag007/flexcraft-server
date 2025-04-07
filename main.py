from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from zstd_asgi import ZstdMiddleware

from crypt.auth_utils import settings
from middlewares.extract_request import RequestMiddleware
from middlewares.file_validator_middleware import FileValidationMiddleware

#
# App
#
app = FastAPI(
    docs_url="/docs",
    swagger_ui_init_oauth={
        "appName": "Credentialing API",
        "clientId": settings.client_id,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

origins = [
    "*"
    # "https://app-staging.billimd.com",
    # "http://localhost:3000",
    # "http://localhost:45678",
    # "http://127.0.0.1:45678",
    # "https://dev-api.billimd.com",
    # "https://app-dev.billimd.com",
    # "https://admin-dev.billimd.com",
    # "https://www-dev.billimd.com",
    # "https://admin.billimd.com",
    # "https://dev.d3bscz9pc3c2oq.amplifyapp.com",
    # "https://app.billimd.com",
    # "https://billimd.com",
    # "https://www.billimd.com",
    # "https://production.d1tvcjkuayvnda.amplifyapp.com",
    # "https://development-v1-0.d1mkkwffns3cnn.amplifyapp.com",
    # "https://dev.d3oanva89hwsuh.amplifyapp.com",
    # "https://promo.billimd.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     ZstdMiddleware,
#     minimum_size=500,
#     write_checksum=True,
#     write_content_size=True,
#     gzip_fallback=True,
# )

app.add_middleware(RequestMiddleware)
app.add_middleware(FileValidationMiddleware)


# init_auth_routes(app)
