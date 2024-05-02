from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

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

# def get_sales_checks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
#     return db.query(models.SalesCheck).filter(models.SalesCheck.user_id == user_id).offset(skip).limit(limit).all()
#
#
# def create_sales_check(db: Session, sales_check: schemas.SalesCheckCreate, user_id: int):
#     db_sales_check = models.SalesCheck(user_id=user_id, **sales_check.dict())
#     db.add(db_sales_check)
#     db.commit()
#     db.refresh(db_sales_check)
#     return db_sales_check