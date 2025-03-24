"""main.py"""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from services.ai_agents.ai_agents import AIAgents
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting backend!")
    yield
    logging.info("Stopping backend")


app = FastAPI(
    lifespan=lifespan,
    title="Paralegal AI",
    version="0.0.1",
)


@app.post("/")
async def test(query: str):
    agents = AIAgents()
    result = await agents.process_query(
        query=query,
    )
    return result


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
