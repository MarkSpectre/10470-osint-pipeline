from collectors.twitter_collector import fetch_twitter 
from collectors.reddit_collector import fetch_reddit 
from collectors.facebook_collector import fetch_facebook 
from collectors.instagram_collector import fetch_instagram
from collectors.tiktok_collector import fetch_tiktok 
# from collectors.linkedin_collector import fetch_linkedin 
from collectors.telegram_collector import fetch_telegram 
#from collectors.discord_collector import messages 
from collectors.mastodon_collector import fetch_mastodon 
from collectors.github_collector import fetch_github 
from collectors.quora_collector import fetch_quora 
from utils.user_details_collector import enrich_user_data
from utils.database import save_user_details, init_db
from collectors.vk_collector import fetch_vk 
from collectors.snapchat_collector import fetch_snapchat 
from utils.cleaners import clean_text, filter_english 
from utils.database import save_to_db 
from utils.sentiment import add_sentiment
from utils.user_details_collector import enrich_user_data
from pathlib import Path
import sqlite3
from datetime import datetime
from tabulate import tabulate
from utils.sentiment import save_sentiment_chart

# Set a reliable database path
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db" / "osint_data.db"

def normalize_record(item, platform):
    """Normalize data into a common schema including user info"""
    if not item:
        return None

    # Get basic record info
    record = {
        "platform": platform,
        "user": item.get("user") or item.get("username") or "N/A",
        "username": item.get("username") or "",
        "name": item.get("name") or "",
        "email": item.get("email") or "",
        "profile_pic": item.get("profile_pic") or "",
        "timestamp": item.get("timestamp") or item.get("date") or item.get("created_at"),
        "text": item.get("text") or item.get("caption") or item.get("description") or "",
        "url": item.get("url") or item.get("link") or "",
        "sentiment": None
    }

    # Try to enrich user data
    if record["username"]:
        user_data = enrich_user_data(platform, record["username"])
        if user_data:
            # Update record with enriched data
            record.update({
                "name": user_data.get("name") or record["name"],
                "email": user_data.get("email") or record["email"],
                "profile_pic": user_data.get("profile_pic") or record["profile_pic"]
            })
            
            # Save detailed user info
            save_user_details({
                "platform": platform,
                "username": record["username"],
                "name": user_data.get("name", ""),
                "email": user_data.get("email", ""),
                "profile_pic": user_data.get("profile_pic", ""),
                "bio": user_data.get("bio", ""),
                "location": user_data.get("location", ""),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0)
            }, DB_PATH)

    return record

def print_db_records(limit=20):
    """Print both posts and user details from the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Print posts
    print("\n=== RECENT POSTS ===")
    c.execute("""
        SELECT platform, user, username, name, email, profile_pic, 
               timestamp, text, url, sentiment 
        FROM social_media_posts 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (limit,))
    
    posts = c.fetchall()
    for post in posts:
        platform, user, username, name, email = post[0:5]
        profile_pic, timestamp, text, url, sentiment = post[5:10]
        
        print(f"\nPlatform: {platform}")
        print(f"User: {user}")
        print(f"Username: {username}")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Profile Pic: {profile_pic}")
        print(f"Timestamp: {timestamp}")
        print(f"Text: {text}")
        print(f"URL: {url}")
        print(f"Sentiment: {sentiment}")
        print("-" * 40)
    
    # Print user details
    print("\n=== USER DETAILS ===")
    c.execute("""
        SELECT platform, username, name, email, profile_pic, bio, 
               location, followers, following, last_updated 
        FROM user_details 
        ORDER BY last_updated DESC 
        LIMIT ?
    """, (limit,))
    
    users = c.fetchall()
    if users:
        headers = ["Platform", "Username", "Name", "Email", "Profile Pic", 
                  "Bio", "Location", "Followers", "Following", "Last Updated"]
        print(tabulate(users, headers=headers, tablefmt="grid"))
    
    conn.close()

def run_pipeline(total_records=100):
    data = []

    platforms = [
        ("Twitter", fetch_twitter, ("AI", 50)),  # you can put high limits; we'll slice later
        ("Reddit", fetch_reddit, ("technology", 50)),
        ("Facebook", fetch_facebook, ("cnn", 50)),
        ("Instagram", fetch_instagram, ("gaming", 50)),
        ("TikTok", fetch_tiktok, ("cybersecurity", 50)),
        ("Mastodon", fetch_mastodon, ("ai", 50)),
        ("GitHub", fetch_github, ("leak", 50)),
        ("Snapchat", fetch_snapchat, ("mrbeast",))
        # Add more collectors here as needed
    ]

    print(f"Fetching data from multiple platforms to collect {total_records} total records...")

    for platform_name, fetch_func, args in platforms:
        try:
            platform_data = fetch_func(*args)
            normalized = [normalize_record(d, platform_name) for d in platform_data if d]

            # Calculate how many more records we can take
            remaining = total_records - len(data)
            if remaining <= 0:
                break  # stop if we've already collected enough

            data.extend(normalized[:remaining])  # only take what's needed

        except Exception as e:
            print(f"Error fetching {platform_name}: {e}")

    print(f"Collected {len(data)} records. Cleaning and enriching...")

    # Clean text
    for d in data:
        if d.get("text"):
            d["text"] = clean_text(d["text"])

    # Filter English content
    data = filter_english(data)

    # Ensure only total_records remain
    data = data[:total_records]

    # Add sentiment
    data = add_sentiment(data)
    save_sentiment_chart(data, output_dir="screenshots", filename="sentiment_chart.png")

    # Save to DB
    save_to_db(data, DB_PATH)
    print(f"✅ Saved {len(data)} normalized multi-platform records to database")

if __name__ == "__main__":
    # Initialize database with new schema
    init_db(DB_PATH)

    run_pipeline(100)
    print_db_records(limit=20)

