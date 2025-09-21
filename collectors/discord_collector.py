import discord
import asyncio
import os

messages = []

DISCORD_KEY = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if not message.author.bot:
        messages.append({
            "platform": "discord",
            "user": str(message.author),
            "timestamp": str(message.created_at),
            "text": message.content,
            "url": f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        })

async def fetch_discord_messages():
    await client.start(DISCORD_KEY)
    # Optionally, add timeout to stop after some time
    await asyncio.sleep(10)  # collect messages for 10 seconds
    await client.close()
    return messages

# Example: run in main pipeline
data = asyncio.run(fetch_discord_messages())
print(data)
