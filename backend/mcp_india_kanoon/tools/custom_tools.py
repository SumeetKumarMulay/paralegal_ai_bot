import json
from mcp.types import Tool, TextContent
from enum import Enum
from config import Config
from utilities.models.Ikapi_model import IKapiModel
from services.scrapping_service.scrapping_service import scrap_raw_html
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

            The return result is in the form of json string and should be
            converted back to object before being read.

            1. min_page starts from 0.
            2. max_page ends at 100.
            max_page and min_page are whole numbers i.e they cannot be floats.

            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
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

            To call specific documents first extract docid from the search_database
            result then pass that docid into this tool.
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
                result = IKapiModel.model_validate(result.json())
                result = [
                    {
                        "docid": result.docs[i].tid,
                        "title": result.docs[i].title,
                        "headline": result.docs[i].headline,
                    }
                    for i in range(pagenum, maxpages)
                ]
                # result = [await self.fetch_doc({"docid": v["docid"]}) for v in result]
                return [TextContent(type="text", text=json.dumps(vl)) for vl in result]
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
        formed_url = f"{url}/doc/{docid}/"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                formed_url,
                headers={
                    "Authorization": f"Token {token}",
                    "Accept": "application/json",
                },
                timeout=3000,
            )
            try:
                response.raise_for_status()
                result = await scrap_raw_html(response.json()["doc"])
                # result = IkapiDocModel.model_validate(result.json())
                return [
                    TextContent(
                        type="text",
                        text="\n\n".join(
                            [
                                f"""
                                doc: {result}
                                """
                            ]
                        ),
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
