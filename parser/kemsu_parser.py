import requests
from bs4 import BeautifulSoup
from typing import List, Dict

from config.settings import KEMSU_URL, REQUEST_TIMEOUT

# Fetches news items from the KEMSU website. Returns a list of dictionaries with title, date and url
def fetch_news() -> List[Dict[str, str]]:
    
    try:
        response = requests.get(KEMSU_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_list: List[Dict[str, str]] = []

    # Find all news cards
    news_items = soup.find_all("div", class_="news-item")

    for item in news_items:
        # Title and link
        title_block = item.find("div", class_="title")
        if not title_block:
            continue

        link_tag = title_block.find("a")
        if not link_tag:
            continue

        title = link_tag.text.strip()
        url = link_tag.get("href")

        if not title or not url:
            continue

        # Date
        date_block = item.find("div", class_="date")
        date = date_block.text.strip() if date_block else ""

        news_list.append({
            "title": title,
            "date": date,
            "url": url
        })

    return news_list

# Filters news by query in title (case-insensitive)
def search_news(query: str) -> List[Dict[str, str]]:

    if not query:
        return []

    query = query.lower()
    all_news = fetch_news()

    return [
        news for news in all_news
        if query in news["title"].lower()
    ]


if __name__ == "__main__":
    results = search_news("ярмарка")
    for n in results:
        print(n["date"])
        print(n["title"])
        print(n["url"])
        print()
