# discord_poster.py

from discord import SyncWebhook
from datetime import datetime
from config import WEBHOOK_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def post_to_discord(buckets):
    """
    Send a Discord embed per topic with up to 5 article previews.
    """
    webhook = SyncWebhook.from_url(WEBHOOK_URL)
    utc_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

    for topic, arts in buckets.items():
        if not arts:
            continue

        embed = {
            'title':       f"{topic} — {len(arts)} new articles",
            'description': f"Latest on **{topic}** as of {utc_now}",
            'fields':      []
        }

        for art in arts[:5]:
            snippet = art['summary'][:200].replace('\n', ' ').strip() + '...'
            embed['fields'].append({
                'name':   art['title'],
                'value':  f"{snippet} [Read more]({art['link']})",
                'inline': False
            })

        webhook.send(embed=[embed])
        logger.info(f"Posted {min(5,len(arts))} articles under '{topic}'")
