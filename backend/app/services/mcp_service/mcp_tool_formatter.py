"""
This tool converts mcp tools to open ai tool.

Follow this to learn more: https://openrouter.ai/docs/use-cases/mcp-servers
"""

from mcp.types import Tool
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.shared_params.function_definition import FunctionDefinition
from typing import Dict


def mcp_tool_formatter(tool: Tool) -> ChatCompletionToolParam:

    params: Dict[str, object] = {
        "type": "object",
        "properties": tool.inputSchema["properties"],
        "required": tool.inputSchema["required"],
    }

    converted_tool = ChatCompletionToolParam(
        type="function",
        function=FunctionDefinition(
            name=tool.name,
            description=tool.description,
            parameters=params,
        ),
    )

    return converted_tool
