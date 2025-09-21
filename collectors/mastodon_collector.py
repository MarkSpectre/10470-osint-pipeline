from mastodon import Mastodon 
mastodon = Mastodon( 
 access_token="MRGA0ZwE0Xo0Iz48lW1BDw7paw_uMZO26njLMbM2Ryc", 
 api_base_url="https://mastodon.social" 
) 
def fetch_mastodon(hashtag="osint", limit=10): 
 results = [] 
 posts = mastodon.timeline_hashtag(hashtag, limit=limit)  
 for p in posts: 
    results.append({ 
    "platform": "mastodon", 
    "user": p["account"]["username"], 
    "timestamp": str(p["created_at"]), 
    "text": p["content"],
    "url": p["url"] 
    }) 
 return results 
