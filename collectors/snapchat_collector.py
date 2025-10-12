import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("SNAPCHAT_KEY")

def fetch_snapchat(username="snapchat"):
    if not RAPIDAPI_KEY:
        print("Error: SNAPCHAT_KEY not found")
        return []

    url = "https://snapchat-profile-scraper-api.p.rapidapi.com/profile"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "snapchat-profile-scraper-api.p.rapidapi.com"
    }
    params = {"username": username}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=30)
        res.raise_for_status()
        data = res.json()

        results = [{
            "platform": "snapchat",
            "name": data.get("name", username),
            "username": username,
            "email": "",
            "profile_pic": data.get("snapcodeURL", ""),
            "timestamp": "",
            "text": data.get("publicAccountData", {}).get("bio", ""),
            "url": f"https://www.snapchat.com/add/{username}"
        }]
        return results

    except Exception as e:
        print(f"Snapchat error: {e}")
        return []
