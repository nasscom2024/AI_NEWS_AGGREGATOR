# discord_poster.py
```python
from discord import SyncWebhook
from datetime import datetime
from config import WEBHOOK_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def post_to_discord(buckets, total_articles=35):
    """
    Collect up to `total_articles` from all topics and post them in one or more embeds.
    Splits into multiple embeds if fields exceed Discord's limit (25 per embed).
    """
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    # Flatten all articles across topics
    all_articles = []
    for arts in buckets.values():
        all_articles.extend(arts)

    # Take up to the requested total number of articles
    selected = all_articles[:total_articles]

    # Discord allows max 25 fields per embed
    chunk_size = 25
    for i in range(0, len(selected), chunk_size):
        chunk = selected[i:i + chunk_size]
        embed = {
            'title':       f"Articles {i+1}-{i+len(chunk)} of {len(selected)}",
            'description': f"Aggregated feed summary as of {utc_now}",
            'fields':      []
        }
        for art in chunk:
            snippet = art['summary'][:200].replace('
', ' ').strip() + '...'
            embed['fields'].append({
                'name':   art['title'],
                'value':  f"{snippet} [Read more]({art['link']})",
                'inline': False
            })
        webhook.send(embed=[embed])
        logger.info(f"Posted embed with {len(chunk)} articles (items {i+1} to {i+len(chunk)})")
