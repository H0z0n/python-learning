import asyncio
import time
import httpx


with httpx.Client(timeout=30) as client:
    start = time.time()
    client.get("http://127.0.0.1:8000/sync-task")
    client.get("http://127.0.0.1:8000/sync-task")
    print(f"(sync-task) Ответ: {time.time() - start:.2f} сек.") # (sync-task) Ответ: 10.01 сек.


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        start = time.time()
        await asyncio.gather(
            client.get("http://127.0.0.1:8000/async-task"),
            client.get("http://127.0.0.1:8000/async-task"),
        )
        print(f"(async-task) Ответ: {time.time() - start:.2f} сек.") # (async-task) Ответ: 5.01 сек.


asyncio.run(main())