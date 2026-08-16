from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, UsersDB
from schemas import UserRegister, UserLogin, Token
from security import hash_password, create_token, verify_password

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

    return { "access_token": access_token, "token_type": "bearer" }