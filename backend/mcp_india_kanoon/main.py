from typing import Dict, Any
from contextlib import asynccontextmanager
from mcp.client.stdio import StdioServerParameters
from mcp import ClientSession, stdio_client
from fastapi import FastAPI, status
import logging
import uvicorn


@asynccontextmanager
async def start_session():
    params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    async with stdio_client(params) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            try:
                init_result = session
                yield init_result
            except Exception as e:
                logging.error(f"mcp session error:: {e}", exc_info=True)
            finally:
                logging.info("mcp session terminated.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting India Kanoon MCP!")
    yield
    logging.info("Stopping India kanoon MCP!")


client = FastAPI(
    title="mcp_india_kanoon",
    lifespan=lifespan,
    # include_in_schema=False,
)


@client.get("/list-tools", status_code=status.HTTP_200_OK)
async def lst_tools():
    async with start_session() as session:
        await session.initialize()
        result = await session.list_tools()
        return result


@client.post("/call-tools", status_code=status.HTTP_202_ACCEPTED)
async def cl_tools(name: str, arguments: Dict[str, Any]):
    async with start_session() as session:
        await session.initialize()
        result = await session.call_tool(name, arguments)
        return result


@client.get("/list-resources", status_code=status.HTTP_200_OK)
async def lst_resources():
    async with start_session() as session:
        await session.initialize()
        result = await session.list_resources()
        return result


@client.post("/call-resources", status_code=status.HTTP_202_ACCEPTED)
async def cl_resources(uri: str):
    async with start_session() as session:
        await session.initialize()
        if uri:
            # perform action
            pass


@client.get("/list-prompts", status_code=status.HTTP_200_OK)
async def lst_prompts():
    async with start_session() as session:
        await session.initialize()
        result = await session.list_prompts()
        return result


@client.get("/get-prompts", status_code=status.HTTP_200_OK)
async def gt_prompts(name: str, arguments: Dict[str, str]):
    async with start_session() as session:
        await session.initialize()
        result = await session.get_prompt(name, arguments)
        return result


if __name__ == "__main__":
    uvicorn.run(
        "main:client",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
