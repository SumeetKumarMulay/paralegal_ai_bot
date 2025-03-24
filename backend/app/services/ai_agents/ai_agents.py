"""AIAgents.py"""

import json
import logging
from openai import AsyncOpenAI
from config import Config
from services.mcp_service.mcp_server import MCPIndiaKanoonService
from services.mcp_service.mcp_tool_formatter import mcp_tool_formatter


class AIAgents:
    def __init__(self):
        self.open_ai = AsyncOpenAI(
            base_url=Config.open_ai_url(),
            api_key=Config.open_api_key(),
        )
        self.mcp_service = MCPIndiaKanoonService()
        self.messages = [
            {
                "role": "system",
                "content": """
                    1. You are a legal bot who help people with legal concepts ONLY INDIAN LEGAL CONCEPTS.
                    2. when you get a query from a user you are to treat it as legal question.
                    3. if you want more context you can query the database attached to the search_database tool.
                    4. The database return a list of documents with a title and a headline. You
                    need to analyse each of them to see if they are relevant to the users query.
                    5. If you find document that is relevant you will also find tid attached to
                    the object. You can use that tid and use the fetch_document_with_doc_id_or_tid
                    tool. If you want meta data for the document fetch_document_meta tool.
                    6. You can analyse it. Once you have all the information. You need to send a
                    concise response to the user.
                    """,
            },
        ]
        self.model = Config.ai_model()

    async def process_query(self, query: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": query,
            },
        )
        tool_list = await self.mcp_service.list_tools()
        tool_list = [mcp_tool_formatter(t) for t in tool_list]

        response = await self.open_ai.chat.completions.create(
            model=self.model,
            tools=tool_list,
            messages=self.messages,
        )

        self.messages.append(response.choices[0].message.model_dump())

        final_text = []
        content = response.choices[0].message

        if content.tool_calls is not None:
            tool_name = content.tool_calls[0].function.name
            tool_args = content.tool_calls[0].function.arguments
            tool_args = json.loads(tool_args) if tool_args else {}

            try:
                result = await self.mcp_service.call_tools(
                    tool_name,
                    tool_args,
                )
                final_text.append(f"calling {tool_name}")
            except Exception as e:
                logging.error(f"{AIAgents.__name__} error :: {e}")
                return None

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": content.tool_calls[0].id,
                    "name": tool_name,
                    "content": result,
                }
            )

            response = await self.open_ai.chat.completions.create(
                model=self.model,
                messages=self.messages,
            )

            final_text.append(response.choices[0].message.content)

        else:
            final_text.append(content.content)

        return final_text

    async def query(self, query: str):
        completion = await self.open_ai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
        )
        data = await completion.choices[0].message.content
        return data
