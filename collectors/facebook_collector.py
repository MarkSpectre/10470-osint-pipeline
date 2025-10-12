import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("FACEBOOK_KEY")
RAPIDAPI_HOST = os.getenv("FACEBOOK_RAPID_HOST")

def fetch_facebook(query="pizza", limit=5):
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found")
        return []

    url = f"https://{RAPIDAPI_HOST}/search/places"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"query": query, "limit": str(limit)}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()
        results = []

        for i in data.get("results", [])[:limit]:
            image = i.get("image", {})
            results.append({
                "platform": "facebook",
                "name": i.get("name", ""),
                "username": i.get("username", ""),
                "email": i.get("email", ""),
                "profile_pic": image.get("uri", ""),
                "timestamp": "",
                "text": i.get("type", ""),
                "url": i.get("url", "")
            })
        return results

    except Exception as e:
        print(f"Facebook error: {e}")
        return []
