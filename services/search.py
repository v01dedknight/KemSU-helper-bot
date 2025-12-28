from parser.kemsu_parser import fetch_news

import logging

logger = logging.getLogger(__name__)

# Returns formatted latest news without search
async def get_latest_news(limit: int = 5) -> list[str]:
    logger.info("Fetching latest news")
    
    news = await fetch_news()

    if not news:
        logger.warning("No news returned from parser")
        return []

    formatted = []
    
    for item in news[:limit]:
        formatted.append(
            f'\n\n{item["date"]}\n{item["title"]}'
        )

    logger.info(f"Returning {len(formatted)} news items to handler")
    return formatted