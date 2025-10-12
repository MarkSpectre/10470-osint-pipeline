import os
import requests
from dotenv import load_dotenv
load_dotenv()

RAPIDAPI_KEY = os.getenv("TWITTER_KEY")  # Using the common RAPIDAPI_KEY
TWITTER_BEARER = os.getenv("TWITTER_BEARER_TOKEN")

def fetch_twitter(query="AI", limit=10):
    """
    Fetch tweets from Twitter using RapidAPI or official API
    Returns list of tweets with user info
    """
    if not (RAPIDAPI_KEY or TWITTER_BEARER):
        print("⚠️ Twitter: No API keys found. Check RAPIDAPI_KEY or TWITTER_BEARER_TOKEN in .env")
        return []

    # Try RapidAPI first
    if RAPIDAPI_KEY:
        url = "https://twitter154.p.rapidapi.com/search"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
        }
        params = {"query": query, "limit": str(limit)}
    else:
        # Fallback to official API
        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER}"}
        params = {"query": query, "max_results": limit}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        
        if resp.status_code == 429:
            print("⚠️ Twitter: Rate limit exceeded. Try again later.")
            return []
        elif resp.status_code == 403:
            print("⚠️ Twitter: Authentication failed. Check your API keys.")
            return []
        
        resp.raise_for_status()
        j = resp.json()

        results = []

        # The twitter241 API returns nested structure under "result" → "timeline" → "instructions"
        entries = []
        try:
            entries = j["result"]["timeline"]["instructions"][0]["entries"]
        except (KeyError, TypeError, IndexError):
            # fallback in case structure differs
            entries = j.get("data") or j.get("statuses") or j.get("tweets") or []

        for entry in entries:
            try:
                tweet_result = (
                    entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                )
                user_result = (
                    entry["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]
                )
            except (KeyError, TypeError):
                # Skip invalid entries
                continue

            # ✅ Extract user details
            username = user_result.get("screen_name", "")
            name = user_result.get("name", "")
            profile_pic = (
                user_result.get("profile_image_url_https", "") or
                user_result.get("profile_image_url", "")
            )

            # ✅ Extract post details
            text = tweet_result.get("full_text", "")
            timestamp = tweet_result.get("created_at", "")
            tweet_id = tweet_result.get("id_str", "")

            results.append({
                "platform": "twitter",
                "username": username,
                "name": name,
                "profile_pic": profile_pic,
                "timestamp": timestamp,
                "text": text,
                "url": f"https://twitter.com/{username}/status/{tweet_id}"
            })

        return results

    except requests.exceptions.HTTPError as e:
        print("Twitter241 HTTPError:", resp.status_code, resp.text)
        return []
    except Exception as e:
        print("Twitter241 error:", e)
        return []
