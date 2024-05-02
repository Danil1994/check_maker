from fastapi.security import OAuth2PasswordBearer,
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Настройки для генерации JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Хэширование пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Функция для получения пользователя по имени
def get_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None


# Функция для аутентификации пользователя
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# Зависимость для проверки токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
