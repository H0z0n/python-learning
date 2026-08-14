from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

class CreatePlayer(BaseModel):
    name: str
    hp: int
    level: int = 1 


DATABASE_URL = "postgresql://postgres:root@127.0.0.1:5432/test_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hp = Column(Integer)
    level = Column(Integer, default=1)


class WeaponDB(Base):
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


# Создание игрока и сохранение словаря с параметрами игрока в список -->>
@app.post("/players")
def new_player(player: CreatePlayer, db: Session = Depends(get_db)):
    new_player_db = PlayerDB(name=player.name, hp=player.hp, level=player.level)
    
    db.add(new_player_db)
    db.commit()
    db.refresh(new_player_db)

    return {"message": f"Игрок {new_player_db.name} создан!", "hp": new_player_db.hp, "level": new_player_db.level, "id": new_player_db.id} 


@app.get("/players")
def get_players_list(db: Session = Depends(get_db)):
    return db.query(PlayerDB).all()


@app.get("/players/{id}")
def get_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayerDB).filter(PlayerDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")

    return player


@app.delete("/players/{id}")
def delete_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayerDB).filter(PlayerDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")
    
    db.delete(player)
    db.commit()

    return {"message": "Игрок успешно удалён!", "removed_player": player, "id": id}


@app.get("/weapons/{id}")
def get_weapon_from_id(id: int, db: Session = Depends(get_db)):
    weapon = db.query(WeaponDB).filter(WeaponDB.id == id).first()

    if weapon is None:
        raise HTTPException(status_code=404, detail="Оружие не найдено!")

    return weapon