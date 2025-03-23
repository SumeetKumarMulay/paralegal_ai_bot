from mcp import stdio_server, types
from mcp.server import Server
import asyncio

app = Server("Test")


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
        types.Tool(
            name="calculate_sum",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        )
    ]


@app.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "calculate_sum":
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Tool not found: {name}")


@app.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="www.example.com",
            name="Application Logs",
            mimeType="text/plain",
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    if str(uri) == "file:///logs/app.log":
        log_contents = "logs"
        return log_contents

    raise ValueError("Resource not found")


asyncio.run(create_app())
