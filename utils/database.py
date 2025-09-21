# import os
# import sqlite3
# from pathlib import Path

# def save_to_db(data, db_path):
#     """
#     Save data to SQLite database with robust path handling
#     """
#     # Set default path if not provided
#     if db_path is None:
#         # Create a data directory if it doesn't exist
#         data_dir = Path("data")
#         data_dir.mkdir(exist_ok=True)
#         db_path = data_dir / "osint_data.db"
    
#     # Convert to string if it's a Path object
#     db_path = str(db_path)
    
#     try:
#         # Ensure the directory exists
#         os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
#         # Connect to database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
        
#         # Create table if it doesn't exist
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS social_media_posts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             platform TEXT,
#             user TEXT,
#             timestamp TEXT,
#             text TEXT,
#             url TEXT,
#             sentiment TEXT
#         )
#         ''')
        
#         # Insert data
#         for record in data:
#             cursor.execute('''
#             INSERT INTO social_media_posts (platform, user, timestamp, text, url,extra)
#             VALUES (?, ?, ?, ?, ?)
#             ''', (record['platform'], record['user'], record['timestamp'], record['text'], record['url'],record['sentiment']))
        
#         # Commit and close
#         conn.commit()
#         conn.close()
        
#         print(f"Successfully saved {len(data)} records to {db_path}")
        
#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#         # Try an alternative path as fallback
#         if db_path != ":memory:":
#             print("Trying in-memory database as fallback...")
#             save_to_db(data, ":memory:")
#     except Exception as e:
#         print(f"Error saving to database: {e}")

import sqlite3
from pathlib import Path

def save_to_db(data, db_path):
    """
    Save list of records to SQLite DB.
    Ensures table exists and missing fields don't break insertion.
    """
    # Ensure db directory exists
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Define table columns
    columns = ["platform", "user", "timestamp", "text", "url", "sentiment"]
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Create table if not exists
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS social_media_posts (
                platform TEXT,
                user TEXT,
                timestamp TEXT,
                text TEXT,
                url TEXT,
                sentiment TEXT
            )
        """)
        
        
        for record in data:
            values = [record.get(col, "") for col in columns]
            c.execute(f"""
               INSERT INTO social_media_posts ({', '.join(columns)})
               VALUES ({', '.join('?' for _ in columns)})
            """, values)

        
        conn.commit()
        print(f"✅ Saved {len(data)} normalized multi-platform records to database")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
