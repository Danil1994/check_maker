from typing import Dict, List

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .calculate import response_builder

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_sale_check(db: Session, user: schemas.User, products_list: List[Dict], payment: dict):
    resp = response_builder(products_list=products_list, payment=payment)
    sale_check = models.SaleCheck(
        user_id=user.id,
        products=resp["products"],
        payment=resp["payment"],
        total=resp["total"],
        rest=resp["rest"],
        created_at=resp["datetime"]
    )
    db.add(sale_check)
    db.commit()
    db.refresh(sale_check)
    return sale_check
