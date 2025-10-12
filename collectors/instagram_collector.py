import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("INSTAGRAM_KEY")
RAPIDAPI_HOST = os.getenv("INSTAGRAM_HOST")

def fetch_instagram(hashtag="gaming", limit=5):
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found")
        return []

    url = "https://instagram-scraper-stable-api.p.rapidapi.com/search_hashtag.php"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"hashtag": hashtag}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()

        edges = data.get("posts", {}).get("edges", [])
        results = []

        for edge in edges[:limit]:
            node = edge.get("node", {})
            owner = node.get("owner", {})
            caption = node.get("edge_media_to_caption", {}).get("edges", [])
            text = caption[0]["node"]["text"] if caption else ""

            results.append({
                "platform": "instagram",
                "name": owner.get("full_name", ""),
                "username": owner.get("username", ""),
                "email": "",
                "profile_pic": node.get("display_url", ""),
                "timestamp": node.get("taken_at_timestamp", ""),
                "text": text,
                "url": f"https://www.instagram.com/p/{node.get('shortcode', '')}"
            })
        return results

    except Exception as e:
        print(f"Instagram error: {e}")
        return []
