"""mcp_server.py"""

import logging
import httpx
import json
from config import Config
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource


class MCPIndiaKanoonService:
    def __init__(self):
        self.url = Config.get_mcp_india_kanoon_url()

    async def list_tools(self) -> list[Tool]:
        async with httpx.AsyncClient() as client:
            result = await client.get(f"{self.url}/list-tools", timeout=3000)
            try:
                result.raise_for_status()
                result = result.json()
                t_lt = [Tool.model_validate(v) for v in result["tools"]]
                return t_lt
            except httpx.HTTPStatusError as e:
                logging.error(f"{MCPIndiaKanoonService.__name__} error :: {e}")
                return None
            except httpx.RequestError as e:
                logging.error(f"{MCPIndiaKanoonService.__name__} error :: {e}")
                return None
            finally:
                logging.info(
                    f"{MCPIndiaKanoonService.__name__} :: completed tool fetch"
                )

    async def call_tools(
        self,
        name: str,
        arguments: dict[str, any],
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        async with httpx.AsyncClient() as client:
            result = await client.post(
                f"{self.url}/call-tools",
                params={
                    "name": name,
                },
                data=json.dumps(arguments),
                timeout=3000,
            )

            try:
                result.raise_for_status()
                result = [
                    TextContent(type=v["type"], text=v["text"])
                    for v in result.json()["content"]
                ]
                return result
            except httpx.HTTPStatusError as e:
                logging.error(
                    f"{MCPIndiaKanoonService.__name__} status error:: {e}",
                )
                return None
            except httpx.RequestError as e:
                logging.error(
                    f"{MCPIndiaKanoonService.__name__} request error :: {e}",
                )
                return None
            finally:
                logging.info(
                    f"{MCPIndiaKanoonService.__name__} :: Tool called",
                )
