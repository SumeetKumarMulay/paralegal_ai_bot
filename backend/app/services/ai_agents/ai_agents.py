"""AIAgents.py"""

import json
import logging
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage
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
        self.model = Config.ai_model()
        self.messages = [
            {
                "role": "system",
                "content": """
                    1. You are a legal bot who help people with legal concepts ONLY INDIAN LEGAL CONCEPTS.
                    2. when you get a query from a user you are to treat it as legal question.
                    3. if you want more context you can query the database attached to the search_database tool.
                    4. The database return a list of documents with a title, headline and docid.
                    You need to analyse each of them to see if they are relevant to the users
                    query.
                    5. If you find document that is relevant you will also find docid
                    attached to the object. You can use that docid and use the
                    fetch_document_with_doc_id_or_tid tool. Analyse at least one document in full.
                    6. You can analyse it. Once you have all the information. You need to send a
                    concise response to the user.
                    """,
            },
        ]
        self.final_message = []

    async def _exc_tool(self, tool_name, tool_args):
        match tool_name:
            case "search_database":
                try:
                    result = await self.mcp_service.call_tools(tool_name, tool_args)
                    result = [v.model_dump() for v in result]

                    # Convert list of dictionaries to formatted string
                    result = "\n\n".join(
                        [
                            f"""
                        docid: {json.loads(entry["text"])["docid"]}
                        Title: {json.loads(entry["text"])["title"]}
                        Headline: {json.loads(entry["text"])["headline"]}
                        """
                            for entry in result
                        ]
                    )
                except Exception as e:
                    logging.error(f"{AIAgents.__name__} error :: {e}")
                    result = (
                        "Error processing request."  # Ensure result is always a string
                    )
            case "fetch_document_with_doc_id_or_tid":
                try:
                    result = await self.mcp_service.call_tools(tool_name, tool_args)
                    result = [v.model_dump() for v in result]

                    result = "\n\n".join(
                        [
                            f"""
                        Title: {json.loads(entry["text"])["title"]}
                        Doc: {json.loads(entry["text"])["doc"]}
                        """
                            for entry in result
                        ]
                    )
                except Exception as e:
                    logging.error(f"{AIAgents.__name__} fetch error :: {e}")
                    result = "Error processing request."
            case "fetch_document_meta":
                result = "Metadata fetching not yet implemented."
            case _:
                result = f"Unknown tool: {tool_name}"

        return result

    async def _process_multi_tool_call(self, content: ChatCompletionMessage):
        while content.tool_calls:
            tool_responses = []

            for tool_call in content.tool_calls:
                tool_name = tool_call.function.name
                tool_args = (
                    json.loads(tool_call.function.arguments)
                    if tool_call.function.arguments
                    else {}
                )

                try:
                    result = await self._exc_tool(tool_name, tool_args)
                    tool_responses.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result,
                        }
                    )
                except Exception as e:
                    logging.error(f"{AIAgents.__name__} tool call error :: {e}")

            self.messages.extend(tool_responses)

            response = await self.open_ai.chat.completions.create(
                model=self.model,
                messages=self.messages,
            )
            content = response.choices[0].message
            self.messages.append(content.model_dump())

        return content

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

        content = response.choices[0].message

        if content.tool_calls is not None:
            content = await self._process_multi_tool_call(content)

        self.final_message.append(content.content if content.content else "")
        return self.final_message

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
