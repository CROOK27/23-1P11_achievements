from typing import Annotated
from pydantic import BaseModel, ConfigDict

class InfoUser(BaseModel):
    username: str
    login: str

class CreateType(BaseModel):
    login: str
    login_add: str

class CreateUser (BaseModel):
    username: str
    login: str
    password: str

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    username: str
    login: str
    password: bytes



class TokenInfo(BaseModel):
    access_token: str
    token_type: str