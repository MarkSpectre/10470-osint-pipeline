# import requests 
# def fetch_snapchat(hashtag="news"): 
#  url = f"https://api.snapkit.com/v1/search?query={hashtag}"  
#  try: 
#     r = requests.get(url) 
#     data = r.json() 
#     return [{"platform":"snapchat","user":"unknown",  "timestamp":"N/A","text":str(i),"url":"N/A"}  for i in data] 
#  except: 
#     return [] 

import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("SNAPCHAT_KEY")

def fetch_snapchat(username):
    """
    Fetch Snapchat profile + snaps using RapidAPI service
    """
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found in environment variables")
        return []
    
    url = "https://snapchat-profile-scraper-api.p.rapidapi.com/profile"
    querystring = {"username": username}
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "snapchat-profile-scraper-api.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        if response.status_code != 200:
            print(f"Snapchat API Error: HTTP {response.status_code} - {response.text[:200]}")
            return []
        
        data = response.json()
        results = []
        
        # Extract profile info
        profile_name = data.get("name", username)
        snapcode_url = data.get("snapcodeURL")
        
        public_data = data.get("publicAccountData", {})
        
        # Collect all snap lists (latest stories, highlights, spotlight)
        all_snaps = []
        all_snaps.extend(public_data.get("latestStorySnaps", []))
        all_snaps.extend(public_data.get("curatedHighlightSnaps", []))
        all_snaps.extend(public_data.get("spotlightHightlightSnaps", []))
        
        # Limit to 5 results
        for snap in all_snaps[:5]:
            results.append({
                "platform": "snapchat",
                "user": profile_name,
                "timestamp": snap.get("timestamp", "N/A"),
                "text": snap.get("caption", ""),
                "url": snap.get("mediaUrl") or snapcode_url or "N/A"
            })
        
        # If no snaps available, return just profile info
        if not results:
            results.append({
                "platform": "snapchat",
                "user": profile_name,
                "timestamp": "N/A",
                "text": public_data.get("bio") or "No snaps available",
                "url": snapcode_url or "N/A"
            })
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Snapchat API: {e}")
        return []
