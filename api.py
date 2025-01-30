from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import *
from enum import Enum
from random import random
app = FastAPI()

class UserType(str, Enum):
    teacher = "Учитель"
    student = "Студент"


class CreateUser(BaseModel):
    login : str
    full_name : str
    type : UserType

@app.post("/user/{user_id}")
async def create_user(user_id: int, user_data: CreateUser):
    user = User.get_or_none(id = user_id)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail=f"Пользователь с ID={user_id} не найден")
    password=