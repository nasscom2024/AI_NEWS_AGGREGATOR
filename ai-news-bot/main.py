# main.py

import logging
from fetcher import fetch_articles
from classifier import classify_articles
from discord_poster import post_to_discord
from config import settings

def main():
    # ——— Logging setup ———
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    logger.info("Starting AI News Bot pipeline")

    # 1) Fetch articles
    logger.info(f"Fetching articles from {len(settings.rss_feeds)} feeds")
    articles = fetch_articles()
    logger.info(f"Fetched {len(articles)} articles")

    # 2) Classify into topics
    logger.info(f"Classifying articles into {len(settings.topic_labels)} topics + Other")
    buckets = classify_articles(articles)
    total_bucketed = sum(len(v) for v in buckets.values())
    logger.info(f"Classification complete: {total_bucketed} articles bucketed")

    # 3) Post to Discord
    logger.info(f"Posting to Discord channel ID {settings.discord_channel_id}")
    post_to_discord(buckets, max_per_topic=5)
    logger.info("Finished posting. Exiting.")

if __name__ == "__main__":
    main()
