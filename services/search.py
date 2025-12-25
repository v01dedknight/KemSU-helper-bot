from parser.kemsu_parser import fetch_news

# Returns formatted latest news without search
def get_latest_news(limit: int = 5) -> list[str]:

    news = fetch_news()

    formatted = []
    for item in news[:limit]:
        formatted.append(
            f'\n\n{item["date"]}\n{item["title"]}'
        )

    return formatted
