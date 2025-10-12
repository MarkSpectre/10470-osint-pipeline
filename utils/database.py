import sqlite3
from pathlib import Path
from datetime import datetime

def init_db(db_path):
    """Initialize database with required tables"""
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create posts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS social_media_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            user TEXT,
            username TEXT,
            name TEXT,
            email TEXT,
            profile_pic TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment REAL
        )
    """)

    # Create user_details table
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            username TEXT,
            name TEXT,
            email TEXT,
            profile_pic TEXT,
            bio TEXT,
            location TEXT,
            followers INTEGER DEFAULT 0,
            following INTEGER DEFAULT 0,
            last_updated TEXT,
            UNIQUE(platform, username)
        )
    """)

    # Create history table to preserve user detail snapshots (append-only)
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_details_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            username TEXT,
            name TEXT,
            email TEXT,
            profile_pic TEXT,
            bio TEXT,
            location TEXT,
            followers INTEGER DEFAULT 0,
            following INTEGER DEFAULT 0,
            last_updated TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_user_details(user_data, db_path):
    """Save or update user details in the database"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Add current timestamp
    user_data["last_updated"] = datetime.now().isoformat()

    # Insert or update user details
    columns = ["platform", "username", "name", "email", "profile_pic", 
               "bio", "location", "followers", "following", "last_updated"]
    
    placeholders = ", ".join("?" * len(columns))
    update_stmt = ", ".join(f"{col} = ?" for col in columns)
    values = [user_data.get(col, "") for col in columns]

    # Insert or update current user_details
    # If a row exists for platform+username, update it; otherwise insert
    try:
        c.execute(f"SELECT id FROM user_details WHERE platform = ? AND username = ?", 
                  (user_data['platform'], user_data['username']))
        existing = c.fetchone()
        if existing:
            # Update existing current record
            c.execute(f"""
                UPDATE user_details 
                SET {update_stmt}
                WHERE platform = ? AND username = ?
            """, values + [user_data["platform"], user_data["username"]])
        else:
            c.execute(f"""
                INSERT INTO user_details ({", ".join(columns)})
                VALUES ({placeholders})
            """, values)
    except Exception as e:
        print(f"Error saving user_details: {e}")

    # Always append to history table (preserve snapshots)
    try:
        hist_cols = columns
        hist_placeholders = ", ".join("?" for _ in hist_cols)
        hist_values = [user_data.get(col, "") for col in hist_cols]
        c.execute(f"INSERT INTO user_details_history ({', '.join(hist_cols)}) VALUES ({hist_placeholders})", hist_values)
    except Exception as e:
        print(f"Error saving user_details_history: {e}")

    conn.commit()
    conn.close()

def get_user_details(platform, username, db_path):
    """Retrieve user details from the database"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        SELECT platform, username, name, email, profile_pic, bio, 
               location, followers, following, last_updated 
        FROM user_details 
        WHERE platform = ? AND username = ?
    """, (platform, username))
    
    row = c.fetchone()
    conn.close()

    if row:
        columns = ["platform", "username", "name", "email", "profile_pic", 
                  "bio", "location", "followers", "following", "last_updated"]
        return dict(zip(columns, row))
    return None

def save_to_db(data, db_path):
    """Save social media posts and user details to database"""
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Initialize database tables
    init_db(db_path)

    columns = [
        "platform", "user", "username", "name", "email",
        "profile_pic", "timestamp", "text", "url", "sentiment"
    ]

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Attempt to add missing columns if any
        existing_cols = [r[1] for r in c.execute("PRAGMA table_info(social_media_posts);").fetchall()]
        for col in columns:
            if col not in existing_cols:
                try:
                    c.execute(f"ALTER TABLE social_media_posts ADD COLUMN {col} TEXT;")
                    print(f"✅ Added missing column: {col}")
                except sqlite3.OperationalError:
                    pass  # ignore if already exists

        for record in data:
            username = record.get("username", "")
            name = record.get("name", "")
            email = record.get("email", "")
            profile_pic = record.get("profile_pic", "")
            platform = record.get("platform", "")
            text = record.get("text", "")
            timestamp = record.get("timestamp", "")
            url = record.get("url", "")

            # (Append-only) We no longer skip duplicates here; always insert new post rows

            if not any([username, name, profile_pic]):
                print(f"⚠️ Warning: Missing username/name/profile_pic for a record on {platform}")

            values = [record.get(col, "") for col in columns]
            # Ensure sentiment is stored as float or NULL
            try:
                if values[-1] == "":
                    values[-1] = None
                else:
                    values[-1] = float(values[-1])
            except Exception:
                values[-1] = None

            c.execute(f"""
                INSERT INTO social_media_posts ({', '.join(columns)})
                VALUES ({', '.join('?' for _ in columns)})
            """, values)

        conn.commit()
        # Count rows in social_media_posts to show appended records (quick feedback)
        inserted = c.execute("SELECT COUNT(*) FROM social_media_posts").fetchone()[0]
        print(f"✅ Saved records. total rows in social_media_posts={inserted}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()
