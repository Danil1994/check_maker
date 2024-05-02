from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
