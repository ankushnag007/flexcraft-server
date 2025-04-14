from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from pydantic import SecretStr

# from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from constants.common import ExceptionType
from genric.encrypt import PasswordCipher
from genric.serializer import custom_jsonable_encoder
from schemas.auth import Login, RefreshToken, Register, ResetPassword
from services.authentication import create_access_token, create_refresh_token, verify_token
from services.email import send_mail_html

from . import user_collection


class RegisterResponse:
    async def create(self, register_dto: Register):
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
    async def create(self, login_dto: Login):
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
    async def create(self, refresh_token: RefreshToken):
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
    def create(self, reset_password_dto: ResetPassword):
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