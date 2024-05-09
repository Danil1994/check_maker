from fastapi import Depends, FastAPI

from main_app import models
from main_app.database import engine, get_db
from main_app.routers import endpoints

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
db = Depends(get_db)
app.include_router(endpoints.router)
