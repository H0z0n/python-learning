from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, WeaponsDB

router = APIRouter()


@router.get("/weapons/{id}")
def get_weapon_from_id(id: int, db: Session = Depends(get_db)):
    weapon = db.query(WeaponsDB).filter(WeaponsDB.id == id).first()

    if weapon is None:
        raise HTTPException(status_code=404, detail="Оружие не найдено!")

    return weapon