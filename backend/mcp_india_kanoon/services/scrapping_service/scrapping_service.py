from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import CrawlerRunConfig
import logging


async def scrap_raw_html(html: str):
    raw_html_url = f"raw:{html}"
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
    )
    async with AsyncWebCrawler() as scraper:
        await scraper.awarmup()
        result = await scraper.arun(raw_html_url, config)
        if result.success:
            logging.info("Scrapping success!")
            return result.markdown
        else:
            logging.info("Scrapping failure!")
            return None
