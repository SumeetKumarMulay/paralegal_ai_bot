from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig
import logging


class ScrappingService:

    @staticmethod
    async def scrap_raw_html(html: str):
        raw_html_url = f"raw:{html}"
        config = CrawlerRunConfig(bypass_cache=True)
        async with AsyncWebCrawler() as scraper:
            result = await scraper.arun(raw_html_url, config)
            if result.success:
                logging.info("Scrapping success!")
                return result.markdown
            else:
                logging.info("Scrapping failure!")
                return None
