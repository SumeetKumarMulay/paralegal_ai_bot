"""main.py"""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
import httpx
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting backend!")
    yield
    logging.info("Stopping backend")


app = FastAPI(lifespan=lifespan, title="Paralegal AI", version="0.0.1")


@app.get("/")
async def test():
    async with httpx.AsyncClient() as client:
        result = await client.get(
            "http://mcp_india_kanoon:8000/list-resources",
        )
        return result.json()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
