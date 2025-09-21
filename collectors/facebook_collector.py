import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("FACEBOOK_KEY")
RAPIDAPI_HOST = os.getenv("FACEBOOK_RAPID_HOST")

def fetch_facebook(query="pizza", limit=5):
    """
    Collector function: fetch Facebook data using RapidAPI Facebook Scraper.
    Returns profile/page details from search results.
    """
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found in environment variables")
        return []

    url = f"https://{RAPIDAPI_HOST}/search/places"
    querystring = {"query": query, "limit": str(limit)}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("results", [])[:limit]:
            image_info = item.get("image", {})
            results.append({
                "platform": "facebook",
                "type": item.get("type"),
                "name": item.get("name"),
                "facebook_id": item.get("facebook_id"),
                "url": item.get("url"),
                "profile_url": item.get("profile_url"),
                "is_verified": item.get("is_verified", False),
                "image_url": image_info.get("uri"),
                "image_width": image_info.get("width"),
                "image_height": image_info.get("height"),
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Facebook API: {e}")
        return []
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return []



