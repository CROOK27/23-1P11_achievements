from core import model
from jwt import InvalidTokenError
from fastapi import Depends, Form, HTTPException, status
from API.api_v1.users.schemas import UserSchema, TokenInfo, CreateUser, CreateType
from API.api_v1.auth import utils as auth_utils
from fastapi.security import OAuth2PasswordBearer
from API.api_v1.auth.utils import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

def create_user(user: CreateUser):
    if not user or model.User.get_or_none(model.User.login == user.login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        ) 
    model.User.get_or_create(
        username=user.username,
        login=user.login,
        password=hash_password(user.password),

    )
    return user

def create_student(user: CreateType):
    if not model.User.get_or_none(model.User.login == user.login_add):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or does not exist"
            )
    main_user = model.User.get_or_none(model.User.login == user.login)
    if not main_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with login {user.login} not found"
        )
    
    adding_user = model.User.get_or_none(model.User.login == user.login_add)
    if not adding_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with login {user.login_add} not found"
        )
    
    if model.Student.get_or_none(model.Student.user == main_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already a student"
        )

    student = model.Student.create(
        user=main_user.id,
        add_teacher=adding_user.id
    )
    
    return student

def create_teacher(user: CreateType):
    if not model.User.get_or_none(model.User.login == user.login_add):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or does not exist"
            )
    main_user = model.User.get_or_none(model.User.login == user.login)
    if not main_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with login {user.login} not found"
        )
    
    adding_user = model.User.get_or_none(model.User.login == user.login_add)
    if not adding_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with login {user.login_add} not found"
        )
    
    if model.Teacher.get_or_none(model.Teacher.user == main_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already a teacher"
        )

    teacher = model.Teacher.create(
        user=main_user.id,
        add_teacher=adding_user.id
    )
    
    return teacher

def validate_auth_user(   
    username: str = Form(...),
    password: str = Form(...)
    ):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"}
    )
    user = model.User.get_or_none(model.User.username == username)
    if not user:
        raise unauthed_exception
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password
    ):
        raise unauthed_exception
    
    return user

def get_current_token_payload_user(
    token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )
    return payload

def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload_user)
) -> UserSchema:
    username : str | None = payload.get("sub")
    if user := model.User.get_or_none(model.User.username == username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
        headers={"WWW-Authenticate": "Basic"}
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_UNAUTHORIZED,
        detail="Inactive user",
    )