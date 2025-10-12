from telethon import TelegramClient 
import os 
from dotenv import load_dotenv 
load_dotenv() 
api_id = int(os.getenv("TELEGRAM_API_ID")) 
api_hash = os.getenv("TELEGRAM_API_HASH") 
client = TelegramClient("osint_session", api_id, api_hash) 
async def fetch_telegram(channel="osint_channel", limit=20):  
   results = []
   async for msg in client.iter_messages(channel, limit=limit):
      results.append({
         "platform": "telegram",
         "user": str(msg.sender_id),
         "username": getattr(msg.sender, "username", ""),
         "name": getattr(msg.sender, "first_name", ""),
         "email": "",
         "profile_pic": getattr(msg.sender, "photo", ""),
         "timestamp": str(msg.date),
         "text": msg.text,
         "url": f"https://t.me/{channel}/{msg.id}"
      })
   return results
         
