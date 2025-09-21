import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("TIKTOK_KEY")

def fetch_tiktok(keyword="cybersecurity", limit=5):
    """
    Fetch TikTok videos using RapidAPI service (updated for correct response format)
    """
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found in environment variables")
        return []
    
    url = "https://tiktok-api23.p.rapidapi.com/api/search/video"
    querystring = {
        "keyword": keyword,
        "cursor": 0,
        "search_id": 0
    }
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "tiktok-api23.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code != 200:
            print(f"TikTok API Error: HTTP {response.status_code} - {response.text[:200]}")
            return []
        
        data = response.json()
        items = data.get("item_list", [])[:limit]  # Use correct key
        results = []
        
        for item in items:
            author_id = item.get("author", {}).get("uniqueId", "unknown")
            video_id = item.get("id", "")
            video_data = item.get("video", {})
            
            results.append({
                "platform": "tiktok",
                "user": author_id,
                "timestamp": item.get("createTime", "N/A"),
                "text": item.get("desc", ""),
                "url": f"https://www.tiktok.com/@{author_id}/video/{video_id}",
                "cover": video_data.get("cover") or "N/A",
                "play_url": video_data.get("playAddr") or "N/A",
                "download_url": video_data.get("downloadAddr") or "N/A"
            })
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TikTok API: {e}")
        return []
