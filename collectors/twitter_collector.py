import os
import requests
from dotenv import load_dotenv

load_dotenv()
TWITTERAPI_IO_KEY = os.getenv("TWITTER_IO_KEY")

def fetch_twitter(query="AI", limit=10):
    """
    Fetch Twitter data using twitterapi.io service
    """
    if not TWITTERAPI_IO_KEY:
        print("Error: TWITTERAPI_IO_KEY not found in environment variables")
        return []
    
    url = "https://api.twitterapi.io/twitter/community/get_tweets_from_all_community"
    
    params = {
        "query": query,
        "queryType" :"Latest",
        "cursor": ""
    }
    
    headers = {
        "x-api-key": TWITTERAPI_IO_KEY,   # ✅ Correct header
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"Twitter API Error: HTTP {response.status_code} - {response.text[:200]}")
            return []
        
        data = response.json()
        
        results = []
        tweets = data.get("statuses", [])[:limit] or data.get("data", [])[:limit] or data.get("tweets", [])[:limit]
        
        for tweet in tweets:
            text = tweet.get("text") or tweet.get("full_text") or ""
            user = tweet.get("user", {}).get("screen_name", "") if isinstance(tweet.get("user"), dict) else tweet.get("screen_name", "")
            timestamp = tweet.get("created_at", "")
            tweet_id = tweet.get("id_str", "") or str(tweet.get("id", ""))
            
            results.append({
                "platform": "twitter",
                "user": user,
                "timestamp": timestamp,
                "text": text,
                "url": f"https://twitter.com/user/status/{tweet_id}" if tweet_id else ""
            })
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Twitter API Request Error: {e}")
        return []
