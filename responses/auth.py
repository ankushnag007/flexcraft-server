import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError, jwt
from pydantic import SecretStr
from pymongo.errors import DuplicateKeyError
from requests_oauthlib import OAuth2Session

from constants.common import ExceptionType
from genric.encrypt import PasswordCipher
from genric.serializer import custom_jsonable_encoder
from schemas.auth import GoogleRegister, Login, RefreshToken, Register, ResetPassword
from services.authentication import create_access_token, create_refresh_token, verify_token
from services.email import send_mail_html

from . import user_collection


class RegisterResponse:
    async def create(self, register_dto: Register, request: Request):
        try:
            register_info_dict = register_dto.model_dump()
            passwd_hash = PasswordCipher.encrypt_password(register_info_dict["password"].get_secret_value())
            register_info_dict["password"] = passwd_hash
            user_collection.insert_one(register_info_dict)
            register_info_dict["password"] = str(SecretStr(passwd_hash))
            access_token = create_access_token({"sub": str(register_info_dict["_id"])})
            refresh_token = create_refresh_token({"sub": str(register_info_dict["_id"])})
            return JSONResponse(status_code=201, content={
                "type": ExceptionType.SUCCESS,
                "message": "user created successfully!",
                "data": custom_jsonable_encoder(register_info_dict),
                "refresh_token": refresh_token,
                "access_token": access_token,
                "token_type": "bearer"
            })
        except DuplicateKeyError as e:
            raise HTTPException(status_code=400, detail={
                "type": ExceptionType.DB_DUPLICACY,
                "message": str(e)
            })
        except Exception as e:
            raise HTTPException(status_code=400, detail={
            "type": ExceptionType.API,
            "message": str(e)
        }
    )
    
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
                    "type": ExceptionType.SUCCESS,
                    "message": "user login successfully!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "type": ExceptionType.API,
                "message": str(e)
            })
    

class RefreshTokenResponse:
    async def create(self, refresh_token: RefreshToken, request: Request):
        try:
            payload = verify_token(refresh_token.refresh_token, expected_type="refresh")
            if not payload: 
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user_id = payload.get("sub")
            new_access_token = create_access_token({"sub": user_id})
            return JSONResponse(
                status_code=201, content={"type": ExceptionType.SUCCESS, "message": "new token generated successfully!", "access_token": new_access_token, "token_type": "bearer"}
            ) 
        except JWTError:
            raise HTTPException(status_code=401, detail={"type": ExceptionType.API,
                "message":"Invalid refresh token"})
        except Exception as e:
            raise HTTPException(status_code=400, detail={
                "type": ExceptionType.API,
                "message": str(e)
            })


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
                    "type": ExceptionType.SUCCESS,
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
                        raise HTTPException(status_code=400, detail={"type": ExceptionType.API, "message": user_info["error"]})
                    user_info_dict = {
                        "email": user_info.get("email"),
                        "first_name": user_info.get("given_name"),
                        "last_name": user_info.get("family_name"),
                        "picture": user_info.get("picture"),
                        "is_google_login": True,
                        "is_verified": user_info.get("verified_email", False),
                    }
                    registration_info = GoogleRegister(**user_info_dict)
                    registration_info_dict = registration_info.model_dump()
                    user_collection.insert_one(registration_info_dict)
                    access_token = create_access_token({"sub": str(registration_info_dict["_id"])})
                    refresh_token = create_refresh_token({"sub": str(registration_info_dict["_id"])})

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

        except Exception as e:
            raise HTTPException(status_code=400, detail={"type": ExceptionType.API, "message": str(e)})
