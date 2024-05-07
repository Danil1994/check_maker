from fastapi import Body
from pydantic import BaseModel, Field
from typing import Annotated, Optional, List, Dict, Union
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


##################################################################

class SaleCheck(BaseModel):
    id: int
    user_id: int
    products: List[Dict[str, Union[str, float, int]]]
    payment: Dict[str, float]
    created_at: Annotated[datetime, Body()]

    class Config:
        orm_mode = True


class SaleCheckCreate(BaseModel):
    products: List[Dict[str, Union[str, float, int]]]
    payment: Dict[str, Union[str, float]]

    products: List[Dict[str, Union[str, float, int]]] = Field(example=[
        {"name": "product1", "price": 10.0, "quantity": 2},
        {"name": "product2", "price": 15.0, "quantity": 1}
    ])
    payment: Dict[str, Union[str, float]] = Field(example={"type": "cash", "amount": 100.0})
