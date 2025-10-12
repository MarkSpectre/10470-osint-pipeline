import praw, os
from dotenv import load_dotenv

load_dotenv()
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")

reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="osint_lab"
)

def fetch_reddit(subreddit="technology", limit=10):
    results = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        author = post.author
        results.append({
            "platform": "reddit",
            "name": getattr(author, "name", ""),
            "username": getattr(author, "name", ""),
            "email": "",
            "profile_pic": getattr(author, "icon_img", ""),
            "timestamp": str(post.created_utc),
            "text": post.title,
            "url": f"https://reddit.com{post.permalink}"
        })
    return results
