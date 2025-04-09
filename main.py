from fastapi import FastAPI
from API.api_v1.users.views import router as user_roken
from core.model import db
import asyncio
import uvicorn
from peewee import SqliteDatabase
from contextlib import asynccontextmanager

db = SqliteDatabase('sqlite.db')

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()

    yield
    db.close()

app = FastAPI(lifespan=lifespan)
app.include_router(user_roken)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)