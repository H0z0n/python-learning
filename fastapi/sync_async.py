import asyncio
import time
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync-task")
def sync_task():
    time.sleep(5)
    return { "message": "Синхронная задача выполнена!" }


@app.get("/async-task")
async def async_task():
    await asyncio.sleep(5)
    return { "message": "Асинхронная задача выполнена!" }