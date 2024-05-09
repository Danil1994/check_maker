from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from main_app import crud, schemas
from main_app.crud import create_sale_check, generate_check_text
from main_app.database import get_db
from main_app.dependencies import ACCESS_TOKEN_EXPIRE_MINUTES
from main_app.registr_and_auth import (authenticate_user, create_access_token,
                                       get_user_from_token)

router = APIRouter()


@router.post("/register", response_model=schemas.User)
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, username=user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    created_user = crud.create_user(db, user_data)
    return created_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/check/")
async def check_create(request: schemas.SaleCheckCreate,
                       db: Session = Depends(get_db),
                       user: schemas.User = Depends(get_user_from_token),
                       ):
    created_sale_check = create_sale_check(db=db, user=user, request=request)
    return created_sale_check


@router.get("/check/")
async def checks_get(db: Session = Depends(get_db),
                     user: schemas.User = Depends(get_user_from_token),
                     created_before: Optional[str] = None,
                     created_after: Optional[str] = None,
                     max_sum: Optional[float] = None,
                     min_sum: Optional[float] = None,
                     type_payment: Optional[str] = None,
                     limit: Optional[int] = 10,
                     page: Optional[int] = 1,
                     offset: Optional[int] = 0
                     ):
    checks = crud.get_checks_by_user_id(db, user.id, created_before, created_after, max_sum, min_sum, type_payment,
                                        limit, page, offset)
    if not checks:
        raise HTTPException(status_code=404, detail="Checks not found")
    return checks


@router.get("/check/{check_id}", response_model=schemas.SaleCheck)
def read_check(check_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_user_from_token)):
    check = crud.get_check_by_id(db, check_id)
    if check is None:
        raise HTTPException(status_code=404, detail="Check not found")
    if check.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to access this check")
    return check


@router.get("/text_check/{check_id}/", response_class=PlainTextResponse)
async def get_check_by_id(check_id: int, string_len: int = 32, db: Session = Depends(get_db)):
    check = crud.get_check_by_id(db, check_id)

    check_text = generate_check_text(db, check, string_len)

    return check_text
