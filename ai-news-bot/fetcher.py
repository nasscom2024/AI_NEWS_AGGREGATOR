# fetcher.py

import feedparser
from config import RSS_FEEDS

def fetch_articles():
    """
    Parse all RSS feeds and return a list of articles.
    Each article is a dict with: title, link, summary, published.
    """
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                "title":     entry.get("title", "No title"),
                "link":      entry.get("link", ""),
                "summary":   entry.get("summary", ""),
                "published": entry.get("published", ""),
            })
    return articles
