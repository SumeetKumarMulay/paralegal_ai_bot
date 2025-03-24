import json
from mcp.types import Tool, TextContent
from enum import Enum
from config import Config
import urllib.parse
import httpx
import logging


class CustomToolType(Enum):
    SEARCH_DATABASE = "search_database"
    FETCH_DOC_W_ID = "fetch_document_with_doc_id_or_tid"
    FETCH_DOC_META_W_ID = "fetch_document_meta"


class CustomTools:

    @staticmethod
    def search_database() -> Tool:
        return Tool(
            name=CustomToolType.SEARCH_DATABASE.value,
            description="""
            Search indian law, court judgments and the constitution.

            1. min_page starts from 0.
            2. max_page ends at 100.
            max_page and min_page are whole numbers i.e they cannot be floats.

            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "str"},
                    "min_pages": {"type": "number"},
                    "max_pages": {"type": "number"},
                },
                "required": ["query"],
            },
        )

    @staticmethod
    def fetch_doc() -> Tool:
        return Tool(
            name=CustomToolType.FETCH_DOC_W_ID.value,
            description="""
            This tool can be used to fetch specific documents from the
            database.

            document id can be called docid or tid. It is a whole number
            greater then 0 and whole numbers.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "docid": {"type": "number"},
                },
                "required": ["docid"],
            },
        )

    @staticmethod
    def fetch_doc_meta() -> Tool:
        return Tool(
            name=CustomToolType.FETCH_DOC_META_W_ID.value,
            description="""
            This tool can be used to fetch the meta data for a given docid or
            document.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "docid": {"type": "number"},
                },
                "required": ["docid"],
            },
        )


class CustomToolCalls:

    def __init__(self):
        self.url = Config.get_api_url()
        self.token = Config.get_api_key()

    async def search_database(self, arguments: dict) -> list[TextContent]:
        url = self.url
        token = self.token
        parsed_query = urllib.parse.quote_plus(arguments["query"].encode("utf8"))
        pagenum = arguments.get("min_pages", 0)
        maxpages = arguments.get("max_pages", 10)
        async with httpx.AsyncClient() as client:
            result = await client.post(
                f"{url}/search/?formInput={parsed_query}&pagenum={pagenum}&maxpages={maxpages}",
                headers={
                    "Authorization": f"Token {token}",
                    "Accept": "application/json",
                },
                timeout=3000,
            )
            try:
                result.raise_for_status()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.json()["docs"]),
                    )
                ]
            except httpx.HTTPStatusError as e:
                logging.error(f"Http error while calling api :: {e}")
                return None
            except httpx.RequestError as e:
                logging.error(f"Http api request error :: {e}")
                return None

    async def fetch_doc(self, arguments: dict) -> list[TextContent]:
        url = self.url
        token = self.token
        docid = arguments["docid"]
        formed_url = f"{url}/docid/{docid}/"
        async with httpx.AsyncClient() as client:
            result = await client.post(
                formed_url,
                headers={
                    "Authorization": f"Token {token}",
                    "Accept": "application/json",
                },
                timeout=3000,
            )
            try:
                result.raise_for_status()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.json()),
                    )
                ]
            except httpx.HTTPStatusError as e:
                logging.error(f"Http error while calling api :: {e}")
                return None
            except httpx.RequestError as e:
                logging.error(f"Http api required error :: {e}")
                return None

    async def fetch_doc_meta(self, arguments: dict) -> list[TextContent]:
        url = self.url
        token = self.token
        docid = arguments["docid"]
        formed_url = f"{url}/docmeta/{docid}/"
        async with httpx.AsyncClient() as client:
            result = await client.post(
                formed_url,
                headers={
                    "Authorization": f"Token {token}",
                    "Accept": "application/json",
                },
                timeout=3000,
            )
            try:
                result.raise_for_status()
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result.json()),
                    )
                ]
            except httpx.HTTPStatusError as e:
                logging.error(f"Http error while call api :: {e}")
                return None
            except httpx.RequestError as e:
                logging.error(f"Http api required error :: {e}")
                return None
