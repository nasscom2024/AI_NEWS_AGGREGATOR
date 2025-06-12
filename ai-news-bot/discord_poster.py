# discord_poster.py

import asyncio
import logging
from datetime import datetime

import discord
from config import settings

# ————— Logging setup —————
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def _post_embeddings(buckets: dict[str, list[dict]], max_per_topic: int = 5):
    """
    Internal coroutine: logs in the bot, posts one Embed per topic (up to max_per_topic articles),
    then gracefully closes.
    """
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logger.info(f"Bot logged in as {client.user} (ID: {client.user.id})")
        channel = client.get_channel(settings.discord_channel_id)
        if channel is None:
            logger.error(f"Channel ID {settings.discord_channel_id} not found.")
            await client.close()
            return

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        # Post one embed per topic
        for topic, articles in buckets.items():
            if not articles:
                continue

            embed = discord.Embed(
                title=f"{topic} — {len(articles)} new articles",
                description=f"Latest on **{topic}** as of {now}",
                color=discord.Color.blurple()
            )
            for art in articles[:max_per_topic]:
                snippet = art["summary"].replace("\n", " ").strip()[:200] + "..."
                embed.add_field(
                    name=art["title"],
                    value=f"{snippet} [Read more]({art['link']})",
                    inline=False
                )

            await channel.send(embed=embed)
            logger.info(f"Posted {min(len(articles), max_per_topic)} articles under '{topic}'")

        await client.close()

    # Start the client (blocks until close)
    await client.start(settings.discord_bot_token)

def post_to_discord(buckets: dict[str, list[dict]], max_per_topic: int = 5):
    """
    Synchronous entry point: runs the async poster.
    """
    asyncio.run(_post_embeddings(buckets, max_per_topic))
