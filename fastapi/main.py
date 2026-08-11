from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Задача №1
# @app.get("/")
# def read_root():
#     return {"message": "Привет мир!"}


# @app.get("/weapons/{weapon_name}")
# def get_weapon(weapon_name: str):
#     return {"weapon_name": weapon_name, "status": "Готов к бою!"}


# @app.get("/reload")
# def reloading(weapon_name: str, amount: int = 30):
#     return {"weapon_name": weapon_name, "reloaded_with": amount}


# Задача №2 и №3
class Player(BaseModel):
    name: str
    hp: int
    level: int = 1 

players_db: list = []


@app.post("/players")
def new_player(player: Player):
    players_db.append(player.model_dump())
    return {"message": f"Игрок {player.name} создан!", "hp": player.hp, "level": player.level} 


@app.get("/players")
def get_players_list():
    return players_db


@app.get("/players/{id}")
def get_player_from_id(id: int):
    if id < 0 or id >= len(players_db):
        raise HTTPException(status_code=404, detail="Игрок не найден!")

    return players_db[id]


@app.delete("/players/{id}")
def delete_player_from_id(id: int):
    if id < 0 or id >= len(players_db):
        raise HTTPException(status_code=404, detail="Игрок не найден!")

    removed_player = players_db.pop(id)
    return {"message": "Игрок успешно удалён!", "removed_player": removed_player, "id": id}