import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError, jwt
from pydantic import SecretStr
from pymongo.errors import DuplicateKeyError
from requests_oauthlib import OAuth2Session

from constants.common import DefaultRoles, ExceptionType
from genric.encrypt import PasswordCipher
from genric.serializer import custom_jsonable_encoder
from schemas.auth import (
    GoogleRegister,
    InitialRegister,
    Login,
    RefreshToken,
    Register,
    ResetPassword,
)
from services.authentication import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from services.email import send_mail_html
from utils.generate_unique_code import generate_invite_code, generate_unique_company_id

from . import company_collection, user_collection


class InitRegisterResponse:
    async def create(self, initial_register_dto: InitialRegister, request: Request):
        try:
            initial_register_info_dict = initial_register_dto.model_dump()[
                "user_details"
            ]

            user = user_collection.find_one(
                {"email": initial_register_info_dict["email"]}
            )
            if user:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "type": ExceptionType.DB_DUPLICACY.value,
                        "message": "User with this email already exists.",
                    },
                )
            passwd_hash = PasswordCipher.encrypt_password(
                initial_register_info_dict["password"].get_secret_value()
            )
            initial_register_info_dict["password"] = passwd_hash
            user_collection.insert_one(initial_register_info_dict)
            initial_register_info_dict["password"] = str(SecretStr(passwd_hash))
            access_token = create_access_token(
                {"user_id": str(initial_register_info_dict["_id"])}
            )
            refresh_token = create_refresh_token(
                {"user_id": str(initial_register_info_dict["_id"])}
            )
            return JSONResponse(
                status_code=201,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "user created successfully!",
                    "data": custom_jsonable_encoder(initial_register_info_dict),
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                    "token_type": "bearer",
                },
            )
        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=400,
                detail={"type": ExceptionType.DB_DUPLICACY.value, "message": str(e)},
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={"type": ExceptionType.API, "message": str(e)},
            )


class RegisterResponse:
    async def create(self, register_dto: Register, request: Request):
        try:
            register_info_dict = register_dto.model_dump()
            if register_info_dict["company_details"].get(
                "domain"
            ) and company_collection.find_one(
                {"domain": register_info_dict["company_details"]["domain"]}
            ):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "type": ExceptionType.API.value,
                        "message": "Domain already taken. Please use a different domain.",
                    },
                )
            if register_info_dict["company_details"].get(
                "email"
            ) and company_collection.find_one(
                {"email": register_info_dict["company_details"]["email"]}
            ):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "type": ExceptionType.API.value,
                        "message": "Company already registered with this email. Please use a different email. or update the existing company.",
                    },
                )
            if register_info_dict["user_details"].get("password"):
                passwd_hash = PasswordCipher.encrypt_password(
                    register_info_dict["user_details"]["password"].get_secret_value()
                )
                register_info_dict["user_details"]["password"] = passwd_hash
            try:
                updated_user = user_collection.find_one_and_update(
                    {"_id": register_info_dict["user_details"]["record_id"]},
                    {"$set": {"field_to_update": register_info_dict["user_details"]}},
                    return_document=True,
                )
                if not updated_user:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "type": ExceptionType.API.value,
                            "message": "User not found.",
                        },
                    )
                if updated_user:
                    commpany_id = str(
                        (
                            company_collection.insert_one(
                                {
                                    **register_info_dict["company_details"],
                                    "invite_code": generate_invite_code(
                                        register_info_dict["company_details"].get(
                                            "domain"
                                        )
                                    ),
                                }
                            )
                        ).inserted_id
                    )
                    register_info_dict["company_details"]["_id"] = commpany_id
                    register_info_dict["user_details"]["company_id"] = commpany_id
                    register_info_dict["user_details"] = updated_user

            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "type": ExceptionType.DB_INSERTION.value,
                        "message": str(e),
                    },
                )
            register_info_dict["user_details"]["password"] = str(
                SecretStr(register_info_dict["user_details"]["password"])
            )
            access_token = create_access_token(
                {
                    "user_id": str(register_info_dict["user_details"]["_id"]),
                    "company_id": register_info_dict["company_details"]["_id"],
                }
            )
            refresh_token = create_refresh_token(
                {
                    "user__id": str(register_info_dict["user_details"]["_id"]),
                    "company_id": register_info_dict["company_details"]["_id"],
                }
            )
            return JSONResponse(
                status_code=201,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "user created successfully!",
                    "data": custom_jsonable_encoder(register_info_dict),
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                    "token_type": "bearer",
                },
            )
        except DuplicateKeyError as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.DB_DUPLICACY.value, "message": str(e)})
        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API.value, "message": str(e)})
    
class LoginResponse:
    async def create(self, login_dto: Login, request: Request):
        try:
            login_info_dict = login_dto.model_dump()
            user = user_collection.find_one({"email": login_info_dict["email"]})
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            if PasswordCipher.decrypt_password(user["password"]) != login_info_dict["password"].get_secret_value():
                raise HTTPException(status_code=401, detail="Invalid credentials")
            access_token = create_access_token({"sub": str(user["_id"])})
            refresh_token = create_refresh_token({"sub": str(user["_id"])})
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "user login successfully!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API.value, "message": str(e)})
    

class RefreshTokenResponse:
    async def create(self, refresh_token: RefreshToken, request: Request):
        try:
            payload = verify_token(refresh_token.refresh_token, expected_type="refresh")
            if not payload: 
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user_id = payload.get("sub")
            new_access_token = create_access_token({"sub": user_id})
            return JSONResponse(
                status_code=201,
                content={"type": ExceptionType.SUCCESS.value, "message": "new token generated successfully!", "access_token": new_access_token, "token_type": "bearer"},
            ) 
        except JWTError:
            raise HTTPException(status_code=401, detail={"type": ExceptionType.API.value, "message": "Invalid refresh token"})
        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API.value, "message": str(e)})


class ResetPasswordResponse:
    async def create(self, reset_password_dto: ResetPassword, request: Request):
        try:
            reset_password_info_dict = reset_password_dto.model_dump()
            user = user_collection.find_one({"email": reset_password_info_dict["email"]})
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            if PasswordCipher.decrypt_password(user["password"]) != reset_password_info_dict["old_password"].get_secret_value():
                raise HTTPException(status_code=401, detail="Invalid credentials")
            if reset_password_info_dict["new_password"].get_secret_value() != reset_password_info_dict["confirm_password"].get_secret_value():
                raise HTTPException(status_code=401, detail="New and confirm password not matching")
            new_passwd_hash = PasswordCipher.encrypt_password(reset_password_info_dict["new_password"].get_secret_value())
            user_collection.update_one({"email": reset_password_info_dict["email"]}, {"$set": {"password": new_passwd_hash}})
            return JSONResponse(
                status_code=200,
                content={
                    "type": ExceptionType.SUCCESS.value,
                    "message": "user password updated successfully!",
                },
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API, "message": str(e)})


class GoogleOauthResponse:
    async def read_all(self, request: Request):
        client_id = "540104557426-8u2radldii80dlcou7k4irvl3m59de80.apps.googleusercontent.com"
        authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        scope = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

        redirect_uri = "http://127.0.0.1:8000/google-oauth-callback"
        google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        authorization_url, _ = google.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")
        return RedirectResponse(authorization_url)


class GoogleOauthCallbackResponse:
    async def read_all(self, request: Request):
        try:
            client_id = "540104557426-8u2radldii80dlcou7k4irvl3m59de80.apps.googleusercontent.com"
            client_secret = "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"
            token_url = "https://www.googleapis.com/oauth2/v4/token"
            redirect_uri = "http://127.0.0.1:8000/google-oauth-callback"
            if "code" in request.query_params:
                code = request.query_params["code"]
                async with httpx.AsyncClient() as client:
                    token_response = await client.post(
                        token_url,
                        data={
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "code": code,
                            "redirect_uri": redirect_uri,
                            "grant_type": "authorization_code",
                        },
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                    )

                    token_data = token_response.json()
                    access_token = token_data.get("access_token")

                    # Fetch user info using the access token
                    user_info_response = await client.get(
                        "https://www.googleapis.com/oauth2/v1/userinfo",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                    user_info = user_info_response.json()
                    if user_info.get("error"):
                        raise HTTPException(status_code=400, detail={"type": ExceptionType.API.value, "message": user_info["error"]})
                    user_info_dict = {
                        "email": user_info["email"],
                        "first_name": user_info.get("given_name"),
                        "last_name": user_info.get("family_name"),
                        "picture": user_info.get("picture"),
                        "is_google_login": True,
                        "is_verified": user_info.get("verified_email", False),
                    }
                    user = user_collection.find_one({"email": user_info_dict["email"]})
                    if not user:
                        try:
                            user_info_dict.update({"role": DefaultRoles.SUPER_ADMIN})
                            registration_info = GoogleRegister(**user_info_dict)
                            registration_info_dict = registration_info.model_dump()
                            user_collection.insert_one(registration_info_dict)
                            access_token = create_access_token(
                                {"_id": str(registration_info_dict["_id"])}
                            )
                            refresh_token = create_refresh_token(
                                {"_id": str(registration_info_dict["_id"])}
                            )
                        except DuplicateKeyError as e:
                            raise HTTPException(
                                status_code=400,
                                detail={
                                    "type": ExceptionType.DB_DUPLICACY.value,
                                    "message": str(e),
                                },
                            )

                        except Exception as e:
                            raise HTTPException(
                                status_code=400,
                                detail={"type": ExceptionType.API, "message": str(e)},
                            )

                        return JSONResponse(
                            status_code=201,
                            content={
                                "type": ExceptionType.SUCCESS,
                                "message": "user created successfully!",
                                "data": custom_jsonable_encoder(registration_info_dict),
                                "refresh_token": refresh_token,
                                "access_token": access_token,
                                "token_type": "bearer",
                            },
                        )

                    return JSONResponse(
                        status_code=201,
                        content={
                            "type": ExceptionType.SUCCESS,
                            "message": "user created successfully!",
                            "data": "working on response since in process for now",
                            "refresh_token": "refresh_token",
                            "access_token": "access_token",
                            "token_type": "bearer",
                        },
                    )

        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API.value, "message": str(e)})
