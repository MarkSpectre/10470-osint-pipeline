import discord
import asyncio
import os

DISCORD_KEY = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
messages = []

@client.event
async def on_message(message):
    if not message.author.bot:
        messages.append({
            "platform": "discord",
            "name": message.author.display_name,
            "username": message.author.name,
            "email": getattr(message.author, "email", ""),
            "profile_pic": str(message.author.avatar.url) if message.author.avatar else "",
            "timestamp": str(message.created_at),
            "text": message.content,
            "url": f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        })

async def fetch_discord_messages(timeout=10):
    await client.start(DISCORD_KEY)
    await asyncio.sleep(timeout)
    await client.close()
    return messages
