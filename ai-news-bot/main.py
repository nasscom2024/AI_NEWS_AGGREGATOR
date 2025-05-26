# main.py

from fetcher import fetch_articles
from classifier import classify_articles
from discord_poster import post_to_discord
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("1/3 Fetching articles…")
    articles = fetch_articles()
    logger.info(f"Fetched {len(articles)} articles")

    logger.info("2/3 Classifying articles…")
    buckets = classify_articles(articles)

    logger.info("3/3 Sending to Discord…")
    post_to_discord(buckets)
    logger.info("Done.")

if __name__ == "__main__":
    main()
