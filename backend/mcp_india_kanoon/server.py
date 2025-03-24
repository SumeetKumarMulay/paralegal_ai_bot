from mcp import stdio_server, types
from mcp.server import Server
from tools.custom_tools import CustomTools, CustomToolType, CustomToolCalls
import asyncio
from dotenv import load_dotenv

app = Server("mcp_india_kanoon")

load_dotenv()


async def create_app():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options(),
        )


@app.list_tools()
async def test_tool_1() -> list[types.Tool]:
    return [
        CustomTools.search_database(),
        CustomTools.fetch_doc(),
        CustomTools.fetch_doc_meta(),
    ]


@app.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    calls = CustomToolCalls()
    match name:
        case CustomToolType.SEARCH_DATABASE.value:
            return await calls.search_database(arguments)
        case CustomToolType.FETCH_DOC_W_ID.value:
            return await calls.fetch_doc(arguments)
        case CustomToolType.FETCH_DOC_META_W_ID.value:
            return await calls.fetch_doc_meta(arguments)
        case _:
            raise ValueError(f"Tool not found: {name}")


# @app.list_resources()
# async def list_resources() -> list[types.Resource]:
#     return [
#         types.Resource(
#             uri="www.example.com",
#             name="Application Logs",
#             mimeType="text/plain",
#         )
#     ]


# @app.read_resource()
# async def read_resource(uri: str) -> str:
#     if str(uri) == "file:///logs/app.log":
#         log_contents = "logs"
#         return log_contents

#     raise ValueError("Resource not found")


asyncio.run(create_app())
