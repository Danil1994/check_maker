from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
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


def create_sale_check(db: Session, user: schemas.User, request: schemas.SaleCheckCreate):
    resp = response_builder(request=request)
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


def get_checks_by_user_id(db, user_id: int,
                          created_before: Optional[str] = None,
                          created_after: Optional[str] = None,
                          max_sum: Optional[float] = None,
                          min_sum: Optional[float] = None,
                          type_payment: Optional[str] = None,
                          limit: Optional[int] = 10,
                          page: Optional[int] = 1,
                          offset: Optional[int] = 0,
                          ):
    query = db.query(models.SaleCheck).filter(models.SaleCheck.user_id == user_id)

    if created_before:
        query = query.filter(models.SaleCheck.created_at <= created_before)

    if created_after:
        query = query.filter(models.SaleCheck.created_at >= created_after)

    if max_sum:
        query = query.filter(models.SaleCheck.total <= max_sum)
    if min_sum:
        query = query.filter(models.SaleCheck.total >= min_sum)

    if type_payment:
        query = query.filter(
            func.json_extract(models.SaleCheck.payment, '$.type') == type_payment
        )
    skip = (page - 1) * limit + offset

    query = query.limit(limit).offset(skip)
    query = query.offset(offset)

    return query.all()


def get_check_by_id(db: Session, check_id: int) -> schemas.SaleCheck:
    return db.query(models.SaleCheck).filter(models.SaleCheck.id == check_id).first()


def generate_check_text(db: Session, check: schemas.SaleCheck, string_len: int = 32) -> str:
    def format_string(text: str, total: float, length: int = string_len) -> str:
        total_length = len(f'{total:.2f}')
        formatted_text = f"{text:<{length - total_length}}{total:>{total_length}.2f}\n"

        return formatted_text

    user = get_user(db, check.user_id)
    payment_type = 'Готівка'
    if check.payment["type"] == "cashless":
        payment_type = 'Картка'
    check_text = f"{'=' * string_len}\n"
    check_text += f"{user.username:^{string_len}}\n"
    check_text += f"{'=' * string_len}\n"

    for product in check.products:
        name = product['name']
        quantity = str(product['quantity']) + ' x '
        price = product['price']
        check_text += format_string(quantity, price)
        check_text += format_string(name, product['total'])
        check_text += '-' * string_len + '\n'

    check_text += format_string('СУМА', check.total)
    check_text += format_string(payment_type, check.payment['amount'])
    check_text += format_string('Решта', check.rest)
    check_text += f"{'=' * string_len}\n"
    check_text += f"{check.created_at.center(string_len)}\n"

    check_text += f"{'Дякуємо за покупку!':^{string_len}}\n"

    return check_text
