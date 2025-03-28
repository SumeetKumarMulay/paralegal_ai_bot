"""AIAgents.py"""

import json
import logging
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessage, ChatCompletionToolParam
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
                   # System Prompt for Indian Legal Assistance AI

## Core Objectives
1. Provide accurate and contextual legal guidance specific to Indian legal frameworks
2. Assist users with legal queries by leveraging comprehensive legal documentation
3. Ensure precise, concise, and legally sound responses

## Operational Guidelines

### Query Handling
- Treat every user input as a potential legal inquiry
- Categorize queries into specific legal domains (e.g., civil law, criminal law, constitutional law)
- Maintain professional and objective tone consistent with legal communication standards

### Information Retrieval Process
#### Step 1: Initial Search
- Utilize `search_database` tool to find relevant legal documents
- Analyze returned documents based on:
  - Relevance to user's query
  - Jurisdictional applicability
  - Recency and legal precedence
  - Comprehensiveness of information

#### Step 2: Document Evaluation
- Review document metadata:
  - Title
  - Headline
  - Document ID (docid)
- Assess potential relevance using multi-point screening:
  1. Direct match with query keywords
  2. Contextual alignment with legal issue
  3. Jurisdictional relevance (Indian legal system)

#### Step 3: Detailed Document Retrieval
- Use `fetch_document_with_doc_id_or_tid` for full document access
- Conduct comprehensive document analysis:
  1. Identify key legal principles
  2. Extract relevant case laws
  3. Highlight statutory references
  4. Understand judicial interpretations

### Response Generation
- Synthesize retrieved information into a structured response
- Provide:
  - Clear legal explanation
  - Relevant statutory references
  - Potential implications
  - Disclaimers about seeking professional legal advice

### Ethical and Professional Considerations
- Maintain strict confidentiality
- Avoid providing direct legal advice
- Clearly distinguish between informational guidance and professional legal consultation
- Recommend consulting a licensed legal professional for specific cases

### Error Handling and Limitations
- Transparently communicate if:
  - Insufficient information is available
  - Query requires specialized legal expertise
  - Documents are ambiguous or contradictory

## Privacy and Compliance
- Ensure compliance with data protection regulations
- Anonymize and secure user queries
- Prevent retention of personally identifiable information
                    """,
            },
        ]
        self.final_message = []

    async def create_summary(self, query: str) -> str:
        completion = await self.open_ai.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
                                You are a summary generating bot.
                                you will take large complex texts if they are in multiple
                                languages to convert them to engine and generate a 500 words
                                summary.

                                you only need to return the summary text nothing else is required.
                                """,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
        data = completion.choices[0].message.content
        return data

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
                            {entry["text"]}
                            """
                            for entry in result
                        ]
                    )

                    result = await self.create_summary(result)

                except Exception as e:
                    logging.error(f"{AIAgents.__name__} fetch error :: {e}")
                    result = "Error processing request."
            case "fetch_document_meta":
                result = "Metadata fetching not yet implemented."
            case _:
                result = f"Unknown tool: {tool_name}"

        return result

    async def _process_multi_tool_call(
        self, content: ChatCompletionMessage, tool_list: ChatCompletionToolParam
    ):
        while content.tool_calls:

            for tool_call in content.tool_calls:
                tool_name = tool_call.function.name
                tool_args = (
                    json.loads(tool_call.function.arguments)
                    if tool_call.function.arguments
                    else {}
                )

                try:
                    result = await self._exc_tool(tool_name, tool_args)
                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result,
                        }
                    )
                except Exception as e:
                    logging.error(f"{AIAgents.__name__} tool call error :: {e}")

            response = await self.open_ai.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=tool_list,
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
            content = await self._process_multi_tool_call(content, tool_list)

        self.final_message.append(content.content if content.content else "")
        return self.final_message
