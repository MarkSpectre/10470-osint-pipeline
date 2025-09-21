# from collectors.twitter_collector import fetch_twitter 
# from collectors.reddit_collector import fetch_reddit 
# from collectors.facebook_collector import fetch_facebook 
# from collectors.instagram_collector import fetch_instagram
# from collectors.tiktok_collector import fetch_tiktok 
# from collectors.linkedin_collector import fetch_linkedin 
# from collectors.telegram_collector import fetch_telegram 
# #from collectors.discord_collector import messages 
# from collectors.mastodon_collector import fetch_mastodon 
# from collectors.github_collector import fetch_github 
# from collectors.quora_collector import fetch_quora 
# from collectors.vk_collector import fetch_vk 
# from collectors.snapchat_collector import fetch_snapchat 
# from utils.cleaners import clean_text, filter_english 
# from utils.database import save_to_db 
# from utils.sentiment import add_sentiment
# import os
# from pathlib import Path

# # Set a reliable database path
# BASE_DIR = Path(__file__).parent
# DB_PATH = BASE_DIR / "db" / "osint_data.db"

# # # Ensure the data directory exists
# # os.makedirs(BASE_DIR / "data", exist_ok=True)

# def print_sample_data(platform_name, data, sample_size=5):
#     """Helper function to print sample data from a platform"""
#     print(f"\n=== {platform_name.upper()} SAMPLE DATA ({len(data)} records) ===")
    
#     if not data:
#         print("No data collected")
#         return
        
#     for i, item in enumerate(data[:sample_size]):
#         print(f"\n--- Record {i+1} ---")
#         print(f"Platform: {item.get('platform', 'N/A')}")
#         print(f"User: {item.get('user', 'N/A')}")
#         print(f"Timestamp: {item.get('timestamp', 'N/A')}")
#         print(f"Text: {item.get('text', 'N/A')[:100]}..." if item.get('text') else "Text: None")
#         print(f"URL: {item.get('url', 'N/A')}")

# def normalize_record(item, platform):
#     """Normalize data into a common schema"""
#     if not item:
#         return None
    
#     return {
#         "platform": platform,
#         "user": item.get("user") or item.get("username") or "N/A",
#         "timestamp": item.get("timestamp") or item.get("date") or item.get("created_at"),
#         "text": item.get("text") or item.get("caption") or item.get("description") or "",
#         "url": item.get("url") or item.get("link") or "",
#         "extra": {k: v for k, v in item.items() if k not in ["user","username","timestamp","date","created_at","text","caption","description","url","link"]}
#     }


# def run_pipeline():
#     data = []

#     print("Fetching Twitter...")
#     twitter_data = fetch_twitter("AI", 10)
#     # print_sample_data("Twitter", twitter_data)
#     # data.extend(twitter_data)
#     data.extend([normalize_record(d, "Twitter") for d in twitter_data])


#     print("Fetching Reddit...")
#     reddit_data = fetch_reddit("technology", 10)
#     # print_sample_data("Reddit", reddit_data)
#     # data.extend(reddit_data)
#     data.extend([normalize_record(d, "Reddit") for d in reddit_data])

#     print("Fetching Facebook...")
#     facebook_data = fetch_facebook("cnn", 5)
#     # print_sample_data("Facebook", facebook_data)
#     # data.extend(facebook_data)
#     data.extend([normalize_record(d, "Facebook") for d in facebook_data])


#     print("Fetching Instagram...")
#     instagram_data = fetch_instagram("gaming",5)
#     # print_sample_data("Instagram", instagram_data)
#     # data.extend(instagram_data)
#     data.extend([normalize_record(d, "Instagram") for d in instagram_data])

#     print("Fetching TikTok...")
#     tiktok_data = fetch_tiktok("cybersecurity", 5)
#     # print_sample_data("TikTok", tiktok_data)
#     # data.extend(tiktok_data)
#     data.extend([normalize_record(d, "TikTok") for d in tiktok_data])

#     print("Fetching Mastodon...")
#     mastodon_data = fetch_mastodon("ai", 5)
#     # print_sample_data("Mastodon", mastodon_data)
#     # data.extend(mastodon_data)
#     data.extend([normalize_record(d, "Mastodon") for d in mastodon_data])

#     print("Fetching GitHub...")
#     github_data = fetch_github("leak", 5)
#     # print_sample_data("GitHub", github_data)
#     # data.extend(github_data)
#     data.extend([normalize_record(d, "GitHub") for d in github_data])

#     print("Fetching Snapchat...")
#     snapchat_data = fetch_snapchat("mrbeast")
#     # print_sample_data("Snapchat", snapchat_data)
#     # data.extend(snapchat_data)
#     data.extend([normalize_record(d, "Snapchat") for d in snapchat_data])

#     # Check for None values before processing
#     # print("\n=== CHECKING FOR NONE VALUES ===")
#     # none_count = 0
#     # for i, item in enumerate(data):
#     #     if item is None:
#     #         print(f"Found None at index {i}")
#     #         none_count += 1
#     #     elif item.get("text") is None:
#     #         print(f"Found None text at index {i}: {item}")
#     #         none_count += 1
            
#     # if none_count > 0:
#     #     print(f"Found {none_count} None values in data. Filtering them out...")
#     #     # Filter out None values
#     #     data = [item for item in data if item is not None and item.get("text") is not None]

#     print("Cleaning and enriching data...")
    
#     # Ensure data is a list before processing
#     if data is None:
#         data = []
    
#     # Clean text for records that have text
#     for d in data:
#         if d is not None and "text" in d and d["text"] is not None:
#             d["text"] = clean_text(d["text"])
    
#     # Filter English content
#     data = filter_english(data)
#     if data is None:
#         data = []
    
#     # Add sentiment
#     data = add_sentiment(data)
#     if data is None:
#         data = []
    
#     # Final check before saving
#     if data is None:
#         data = []
    
#     save_to_db(data, DB_PATH)
#     print(f"✅ Collected {len(data)} multi-platform OSINT records")

# if __name__ == "__main__": 
#     run_pipeline()

from collectors.twitter_collector import fetch_twitter 
from collectors.reddit_collector import fetch_reddit 
from collectors.facebook_collector import fetch_facebook 
from collectors.instagram_collector import fetch_instagram
from collectors.tiktok_collector import fetch_tiktok 
from collectors.linkedin_collector import fetch_linkedin 
from collectors.telegram_collector import fetch_telegram 
#from collectors.discord_collector import messages 
from collectors.mastodon_collector import fetch_mastodon 
from collectors.github_collector import fetch_github 
from collectors.quora_collector import fetch_quora 
from collectors.vk_collector import fetch_vk 
from collectors.snapchat_collector import fetch_snapchat 
from utils.cleaners import clean_text, filter_english 
from utils.database import save_to_db 
from utils.sentiment import add_sentiment
from pathlib import Path
import sqlite3
from tabulate import tabulate

# Set a reliable database path
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db" / "osint_data.db"

def normalize_record(item, platform):
    """Normalize data into a common schema"""
    if not item:
        return None
    
    return {
        "platform": platform,
        "user": item.get("user") or item.get("username") or "N/A",
        "timestamp": item.get("timestamp") or item.get("date") or item.get("created_at"),
        "text": item.get("text") or item.get("caption") or item.get("description") or "",
        "url": item.get("url") or item.get("link") or "",
        "sentiment": None  # placeholder, will be filled after sentiment analysis
    }

def print_db_records(table_name="social_media_posts", limit=10):
    """Print records from the SQLite database in table format"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = c.fetchall()
        if not rows:
            print(f"No records found in table '{table_name}'.")
            return
        
        # Get column names
        col_names = [desc[0] for desc in c.description]
        
        # Print as table
        print(tabulate(rows, headers=col_names, tablefmt="grid"))
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

def run_pipeline(total_records=100):
    data = []

    platforms = [
        ("Twitter", fetch_twitter, ("AI", 10)),
        ("Reddit", fetch_reddit, ("technology", 10)),
        ("Facebook", fetch_facebook, ("cnn", 5)),
        ("Instagram", fetch_instagram, ("gaming", 5)),
        ("TikTok", fetch_tiktok, ("cybersecurity", 5)),
        ("Mastodon", fetch_mastodon, ("ai", 5)),
        ("GitHub", fetch_github, ("leak", 5)),
        ("Snapchat", fetch_snapchat, ("mrbeast",))
    ]

    print(f"Fetching data from multiple platforms to store {total_records} records...")

    # Fetch and normalize data
    for platform_name, fetch_func, args in platforms:
        try:
            platform_data = fetch_func(*args)
            normalized = [normalize_record(d, platform_name) for d in platform_data if d]
            data.extend(normalized)
        except Exception as e:
            print(f"Error fetching {platform_name}: {e}")

        # Stop if we reach the desired total records
        if len(data) >= total_records:
            data = data[:total_records]
            break

    print(f"Collected {len(data)} records. Cleaning and enriching...")

    # Clean text
    for d in data:
        if d.get("text"):
            d["text"] = clean_text(d["text"])

    # Filter English content
    data = filter_english(data)

    # Ensure only the top `total_records` remain after filtering
    data = data[:total_records]

    # Add sentiment
    data = add_sentiment(data)

    # Save to DB
    save_to_db(data, DB_PATH)
    print(f"✅ Saved {len(data)} normalized multi-platform records to database")

if __name__ == "__main__":
    run_pipeline(100)
    print_db_records(limit=20)
