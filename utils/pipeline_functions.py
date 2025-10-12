# Function to display user details
def print_user_details(platform=None, limit=10):
    """
    Print detailed user information from the database
    Args:
        platform: Optional filter by platform
        limit: Maximum number of users to display
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = """
        SELECT platform, username, name, email, profile_pic, bio, location, 
               followers, following, last_updated
        FROM user_details
    """
    params = []
    
    if platform:
        query += " WHERE platform = ?"
        params.append(platform)
    
    query += f" LIMIT {limit}"
    
    rows = c.execute(query, params).fetchall()
    conn.close()
    
    if not rows:
        print("No user details found")
        return
        
    headers = ["Platform", "Username", "Name", "Email", "Profile Pic", "Bio", 
              "Location", "Followers", "Following", "Last Updated"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

# Modify the run_pipeline function to collect user details
def run_pipeline(total_records=750):
    data = []
    collected_users = set()  # Track unique users

    platforms = [
        ("Twitter", fetch_twitter, ("AI", 100)),
        ("Reddit", fetch_reddit, ("technology", 100)),
        ("Facebook", fetch_facebook, ("cnn", 80)),
        ("Instagram", fetch_instagram, ("gaming", 30)),
        ("TikTok", fetch_tiktok, ("cybersecurity", 30)),
        ("Mastodon", fetch_mastodon, ("ai", 80)),
        ("GitHub", fetch_github, ("leak", 60)),
        ("Snapchat", fetch_snapchat, ("mrbeast",))
    ]

    print(f"Fetching data from multiple platforms to store {total_records} records...")

    # Fetch and normalize data
    for platform_name, fetch_func, args in platforms:
        try:
            platform_data = fetch_func(*args)
            normalized = [normalize_record(d, platform_name) for d in platform_data if d]
            data.extend(normalized)
            
            # Collect unique users for this platform
            for record in normalized:
                if record and record.get("username"):
                    user_key = (platform_name, record["username"])
                    if user_key not in collected_users:
                        collected_users.add(user_key)
                        # Try to get additional user details
                        user_data = enrich_user_data(platform_name, record["username"])
                        if user_data:
                            save_user_details(user_data, DB_PATH)
                            
        except Exception as e:
            print(f"Error fetching {platform_name}: {e}")

        if len(data) >= total_records:
            data = data[:total_records]
            break

    print(f"Collected {len(data)} records. Cleaning and enriching...")

    # Clean text and filter English content
    for d in data:
        if d.get("text"):
            d["text"] = clean_text(d["text"])
    data = filter_english(data)
    data = data[:total_records]

    # Add sentiment analysis
    data = add_sentiment(data)
    save_sentiment_chart(data, output_dir="screenshots", filename="sentiment_chart.png")

    # Save to database
    save_to_db(data, DB_PATH)
    print(f"✅ Saved {len(data)} normalized multi-platform records to database")