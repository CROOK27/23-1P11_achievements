from fastapi import APIRouter
from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from API.api_v1.users.schemas import UserSchema, TokenInfo, CreateUser, InfoUser
from API.api_v1.auth import utils as auth_utils
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from API.api_v1.users.crud import *

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
    )

@router.post("/create/", response_model=InfoUser)
def create_users(
    user: CreateUser = Depends(create_user)
    ):
    return user

@router.post("/create_student/")
def create_student(
    user: CreateType = Depends(create_student)
    ):
    return user

@router.post("/create_teacher/")
def create_teacher(
    user: CreateType = Depends(create_teacher)
    ):
    return user

@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_paylaod = {
        "sub": user.username,
        "login": user.login
    }
    token = auth_utils.encode_jwt(jwt_paylaod)
    return TokenInfo(
        access_token = token,
        token_type = "Bearer"
    )

@router.get("/me/")
def get_user_me(
    payload: dict = Depends(get_current_token_payload_user),
    user: UserSchema = Depends(get_current_active_auth_user)
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "login": user.login,
        "logged_at": iat,
    }