from pydantic import BaseModel

# Модель пользователя
class User(BaseModel):
    username: str
    password: str


# Модель токена доступа
class Token(BaseModel):
    access_token: str
    token_type: str