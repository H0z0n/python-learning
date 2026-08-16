from fastapi import FastAPI
from database import Base, engine

from routers import auth, players, weapons

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(players.router)
app.include_router(weapons.router)