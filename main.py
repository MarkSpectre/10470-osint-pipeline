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

