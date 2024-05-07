from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from main_app.crud import create_sale_check
from main_app.database import get_db
from main_app.registr_and_auth import get_user_from_token, oauth2_scheme, authenticate_user, create_access_token
from main_app.dependencies import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from main_app import crud, schemas

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


@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_user_from_token)):
    return current_user


@router.post("/process_products/")
async def process_products(request_body: schemas.SaleCheckCreate,
                           db: Session = Depends(get_db),
                           current_user: schemas.User = Depends(get_user_from_token),
                           ):
    products = request_body.products
    payment = request_body.payment

    created_sale_check = create_sale_check(db=db, user=current_user, products_list=products, payment=payment)
    return created_sale_check
