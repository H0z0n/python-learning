from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import CreatePlayer
from database import get_db, UsersDB, PlayersDB
from security import get_current_user

router = APIRouter()


# Создание игрока и сохранение словаря с параметрами игрока в список -->>
@router.post("/players")
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


@router.get("/players")
def get_players_list(db: Session = Depends(get_db)):
    return db.query(PlayersDB).all()


@router.get("/players/{id}")
def get_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayersDB).filter(PlayersDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")

    return player


@router.delete("/players/{id}")
def delete_player_from_id(id: int, db: Session = Depends(get_db)):
    player = db.query(PlayersDB).filter(PlayersDB.id == id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден!")
    
    db.delete(player)
    db.commit()

    return {"message": "Игрок успешно удалён!", "removed_player": player, "id": id}