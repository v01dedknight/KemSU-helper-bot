import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

from config.settings import KEMSU_URL, REQUEST_TIMEOUT

import logging

logger = logging.getLogger(__name__)

# Fetches news items from the KEMSU website. Returns a list of dictionaries with title, date and url
async def fetch_news() -> List[Dict[str, str]]:
    logger.info(f"Requesting {KEMSU_URL}")
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(KEMSU_URL) as response:
            if response.status != 200:
                logger.warning(f"KEMSU returned non-200 status: {response.status}")
                return []

            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    news_list = []

    for item in soup.find_all("div", class_="news-item"):
        title_block = item.find("div", class_="title")
        if not title_block:
            continue

        link = title_block.find("a")
        if not link:
            continue

        date_block = item.find("div", class_="date")

        news_list.append({
            "title": link.text.strip(),
            "url": link["href"],
            "date": date_block.text.strip() if date_block else ""
        })
    logger.info(f"Parsed {len(news_list)} news items")

    return news_list