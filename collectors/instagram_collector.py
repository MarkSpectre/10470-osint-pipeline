import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("INSTAGRAM_KEY")
RAPIDAPI_HOST = os.getenv("INSTAGRAM_HOST")

def fetch_instagram(hashtag="gaming",limit=5):
    """
    Fetch Instagram posts using a RapidAPI service
    """
    if not RAPIDAPI_KEY:
        print("Error: RAPIDAPI_KEY not found in environment variables")
        return []
    
    # These values will vary based on which Instagram API you choose on RapidAPI
    # You'll need to update these based on the specific API's documentation
    url = "https://instagram-scraper-stable-api.p.rapidapi.com/search_hashtag.php"
    
    querystring = {
        "hashtag":hashtag
    }
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST # Update with your API's host
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        edges = data.get("posts", {}).get("edges", [])
        if not edges:
            print("No posts found for this hashtag.")
            return []

        posts = []
        for edge in edges:
            node = edge.get("node")
            if not node:
                continue

            # Caption
            caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
            caption_text = caption_edges[0]["node"]["text"] if caption_edges else ""

            # Post URL
            shortcode = node.get("shortcode", "")
            post_url = f"https://www.instagram.com/p/{shortcode}" if shortcode else ""

            posts.append({
                "platform": "instagram",
                "hashtag": hashtag,
                "timestamp": node.get("taken_at_timestamp"),
                "text": caption_text,
                "url": post_url,
                "display_url": node.get("display_url"),
                "likes": node.get("edge_liked_by", {}).get("count", 0),
                "comments": node.get("edge_media_to_comment", {}).get("count", 0),
                "is_video": node.get("is_video", False)
            })

        return posts[:limit]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Instagram API: {e}")
        return []
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return []