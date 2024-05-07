from enum import Enum
from typing import Dict, List, Union

from sqlalchemy import Boolean, Column, ForeignKey, Integer, JSON, String, Float, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from .database import Base


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    sale_checks = relationship("SaleCheck", back_populates="user")


class SaleCheck(Base):
    __tablename__ = 'sale_checks'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    products = Column(JSON)
    payment = Column(JSON)
    total = Column(Float)
    rest = Column(Float)
    created_at = Column(String)

    user = relationship("User", back_populates="sale_checks")
