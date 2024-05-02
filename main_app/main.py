from fastapi import FastAPI
from main_app.routers import endpoints

from .database import engine
from main_app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(endpoints.router)

from main_app.crud import get_user_by_username
from main_app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

db = Depends(get_db)
print(db)

# get_user_by_username(db, 'user_1')
