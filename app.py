from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import sqlite3
from pathlib import Path
from datetime import datetime
import json
import io
import requests
from PIL import Image
import imagehash
from utils.visualizer import create_platform_stats_chart

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flashing messages

# Path to your SQLite database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "osint_data.db"
CHARTS_DIR = BASE_DIR / "static" / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access rows like dictionaries
    return conn

@app.route("/")
def home():
    """Home page showing all posts as cards with statistics"""
    conn = get_db_connection()
    
    # Get posts with sentiment analysis
    posts = conn.execute("""
        SELECT p.*, u.followers, u.following, u.bio
        FROM social_media_posts p
        LEFT JOIN user_details u 
            ON p.username = u.username 
            AND p.platform = u.platform
        ORDER BY p.timestamp DESC
    """).fetchall()

    # Coerce sentiment to float (fixes TypeError in templates when comparing)
    posts = [dict(post) for post in posts]
    for p in posts:
        s = p.get('sentiment')
        try:
            p['sentiment'] = float(s) if s is not None and s != '' else None
        except (ValueError, TypeError):
            p['sentiment'] = None
    
    # Get platform statistics
    platforms = conn.execute("""
        SELECT DISTINCT platform 
        FROM social_media_posts
    """).fetchall()
    platforms = [p['platform'] for p in platforms]
    
    # Get unique users count
    unique_users = conn.execute("""
        SELECT COUNT(DISTINCT username) as count
        FROM social_media_posts
    """).fetchone()['count']
    
    # Generate platform statistics chart
    create_platform_stats_chart(
        DB_PATH,
        CHARTS_DIR / "platform_stats.png"
    )
    
    conn.close()
    
    return render_template("index.html",
                         posts=posts,
                         platforms=platforms,
                         unique_users=unique_users)


def fetch_image_hash_from_url(url, timeout=8):
    """Download image from URL and compute perceptual hash (phash). Returns imagehash.ImageHash or None."""
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert('RGB')
        return imagehash.phash(img)
    except Exception:
        return None


@app.route('/search_by_image', methods=['GET', 'POST'])
def search_by_image():
    """Search user profiles by uploading a profile image. Compares perceptual hashes against stored profile_pic URLs in user_details."""
    if request.method == 'POST':
        file = request.files.get('image')
        if not file:
            flash('Please upload an image to search.', 'error')
            return redirect(url_for('search_by_image'))

        try:
            img = Image.open(file.stream).convert('RGB')
        except Exception:
            flash('Uploaded file is not a valid image.', 'error')
            return redirect(url_for('search_by_image'))

        target_hash = imagehash.phash(img)

        # Query all user profile_pic URLs from DB
        conn = get_db_connection()
        rows = conn.execute("SELECT platform, username, name, profile_pic FROM user_details WHERE profile_pic IS NOT NULL AND profile_pic != ''").fetchall()
        conn.close()

        matches = []
        for r in rows:
            url = r['profile_pic']
            h = fetch_image_hash_from_url(url)
            if h is None:
                continue
            # Hamming distance threshold: <= 10 is a reasonable starting point for phash (adjustable)
            dist = target_hash - h
            if dist <= 10:
                matches.append({
                    'platform': r['platform'],
                    'username': r['username'],
                    'name': r['name'],
                    'profile_pic': url,
                    'distance': int(dist)
                })

        # Sort by distance ascending
        matches = sorted(matches, key=lambda x: x['distance'])

        # For each matched user, fetch their recent posts and prepare for rendering as cards
        conn = get_db_connection()
        matches_posts = []
        for m in matches:
            posts_rows = conn.execute(
                """
                SELECT * FROM social_media_posts
                WHERE platform = ? AND username = ?
                ORDER BY timestamp DESC
                LIMIT 20
                """,
                (m['platform'], m['username'])
            ).fetchall()

            posts = [dict(p) for p in posts_rows]
            # Coerce sentiment to float for template comparisons
            for p in posts:
                s = p.get('sentiment')
                try:
                    p['sentiment'] = float(s) if s is not None and s != '' else None
                except (ValueError, TypeError):
                    p['sentiment'] = None

            matches_posts.append({
                'match': m,
                'posts': posts
            })

        conn.close()
        return render_template('search_by_image.html', matches_posts=matches_posts, query_count=len(matches_posts))

    return render_template('search_by_image.html', matches=None)

@app.route("/search")
def search():
    """Search by name, username, email, or profile_pic"""
    query = request.args.get("q", "").strip().lower()
    conn = get_db_connection()

    posts = []
    if query:
        posts = conn.execute("""
            SELECT * FROM social_media_posts
            WHERE LOWER(name) LIKE ?
               OR LOWER(username) LIKE ?
               OR LOWER(email) LIKE ?
               OR LOWER(profile_pic) LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
    conn.close()

    # Coerce sentiment to float for template comparisons
    posts = [dict(p) for p in posts]
    for p in posts:
        s = p.get('sentiment')
        try:
            p['sentiment'] = float(s) if s is not None and s != '' else None
        except (ValueError, TypeError):
            p['sentiment'] = None

    return render_template("search.html", posts=posts, query=query)

if __name__ == "__main__":
    app.run(debug=True)
