from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, UsersDB
from schemas import UserRegister, UserLogin, Token, RefreshRequest
from security import hash_password, create_token, create_refresh_token, decode_token, verify_password

router = APIRouter()


# Регистрация и авторизация юзеров -->>
@router.post("/register")
def user_register(user: UserRegister, db: Session = Depends(get_db)):
    new_user = db.query(UsersDB).filter(UsersDB.username == user.username).first()

    if new_user is not None:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует!")

    new_user = UsersDB(username = user.username, hashed_password = hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { "message": f"Зарегистрирован новый пользователь: {new_user.username}", "id": new_user.id }


@router.post("/login", response_model=Token)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UsersDB).filter(UsersDB.username == user.username).first()

    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль!")

    access_token = create_token({"username": db_user.username, "id": db_user.id})
    refresh_token = create_refresh_token({"username": db_user.username, "id": db_user.id})

    return { "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer" }


@router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Невалидный refresh-токен!")

    username = payload.get("username")
    db_user = db.query(UsersDB).filter(UsersDB.username == username).first()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден!")

    new_access_token = create_token({"username": db_user.username, "id": db_user.id})
    new_refresh_token = create_refresh_token({"username": db_user.username, "id": db_user.id})

    return { "access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer" }