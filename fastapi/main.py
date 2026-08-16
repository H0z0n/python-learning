from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CreatePlayer(BaseModel):
    name: str
    hp: int
    level: int = 1 


DATABASE_URL = "postgresql://postgres:root@127.0.0.1:5432/test_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

SECRET_TOKEN = "my-secret-token"
ALGORITHM_TYPE = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class UsersDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class PlayersDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hp = Column(Integer)
    level = Column(Integer, default=1)

class WeaponsDB(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ammo = Column(Integer)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hashed_password(pwd: str) -> str:
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


# Регистрация и авторизация юзеров -->>
@app.post("/register")
def user_register(user: UserRegister, db: Session = Depends(get_db)):
    new_user = db.query(UsersDB).filter(UsersDB.username == user.username).first()
    if new_user is not None:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует!")

    new_user = UsersDB(username = user.username, hashed_password = hashed_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { "message": f"Зарегистрирован новый пользователь: {new_user.username}", "id": new_user.id }


@app.post("/login", response_model=Token)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UsersDB).filter(UsersDB.username == user.username).first()

    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль!")

    access_token = create_token({"username": db_user.username, "id": db_user.id})

    return { "access_token": access_token, "token_type": "bearer" }


# Создание игрока и сохранение словаря с параметрами игрока в список -->>
@app.post("/players")
def new_player(
        player: CreatePlayer, 
        db: Session = Depends(get_db), 
        current_user: UsersDB = Depends(get_current_user)
    ):
    new_player_db = PlayersDB(name=player.name, hp=player.hp, level=player.level)
    
    db.add(new_player_db)
    db.commit()
    db.refresh(new_player_db)

    return {
        "message": f"Игрок {new_player_db.name} создан пользователем: {current_user.username}", 
        "hp": new_player_db.hp, 
        "level": new_player_db.level, 
        "id": new_player_db.id
    } 


@app.get("/players")
def get_players_list(db: Session = Depends(get_db)):
    return db.query(PlayersDB).all()


@app.get("/players/{id}")
def get_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayersDB).filter(PlayersDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")

    return player


@app.delete("/players/{id}")
def delete_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayersDB).filter(PlayersDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")
    
    db.delete(player)
    db.commit()

    return {"message": "Игрок успешно удалён!", "removed_player": player, "id": id}


@app.get("/weapons/{id}")
def get_weapon_from_id(id: int, db: Session = Depends(get_db)):
    weapon = db.query(WeaponsDB).filter(WeaponsDB.id == id).first()

    if weapon is None:
        raise HTTPException(status_code=404, detail="Оружие не найдено!")

    return weapon