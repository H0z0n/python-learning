import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, UsersDB

SECRET_TOKEN = "my-secret-token"
ALGORITHM_TYPE = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def hash_password(pwd: str) -> str:
    pwd_bytes = pwd.encode()
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd.decode()


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    plain_pwd_bytes = plain_pwd.encode()
    hashed_pwd_bytes = hashed_pwd.encode()
    return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)


def create_token(data: dict) -> str:
    copy_data = data.copy()
    expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copy_data.update({"exp": expire_time})
    encoded_jwt = jwt.encode(copy_data, SECRET_TOKEN, ALGORITHM_TYPE)
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, SECRET_TOKEN, ALGORITHM_TYPE)
        return decoded_token
    except JWTError:
        return None


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security), 
        db: Session = Depends(get_db)
    ):
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Невалидный или истёкший токен!")

    username = payload.get("username")
    user_db = db.query(UsersDB).filter(UsersDB.username == username).first()

    if user_db is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден!")

    return user_db
