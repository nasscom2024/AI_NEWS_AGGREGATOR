# fetcher.py

from typing import List, Dict
import feedparser
from config import settings

def fetch_articles() -> List[Dict[str, str]]:
   
    articles: List[Dict[str, str]] = []

    for url in settings.rss_feeds:
        # Parse the RSS/Atom feed at this URL
        feed = feedparser.parse(url)

        for entry in feed.entries:
            articles.append({
                "title":     entry.get("title", "No title"),
                "link":      entry.get("link", ""),
                "summary":   entry.get("summary", ""),
                "published": entry.get("published", ""),
            })

    return articles
