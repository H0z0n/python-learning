from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db, WeaponsDB

router = APIRouter()


@router.get("/weapons/{id}")
def get_weapon_from_id(id: int, db: Session = Depends(get_db)):
    stmt = select(WeaponsDB).where(WeaponsDB.id == id)
    weapon = db.execute(stmt).scalars().first()

    if weapon is None:
        raise HTTPException(status_code=404, detail="Оружие не найдено!")

    return weapon