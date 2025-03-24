"""
This tool converts mcp tools to open ai tool.

Follow this to learn more: https://openrouter.ai/docs/use-cases/mcp-servers
"""

from mcp.types import Tool


def mcp_tool_formatter(tool: Tool):
    converted_tool = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"],
                "required": tool.inputSchema["required"],
            },
        },
    }
    return converted_tool
