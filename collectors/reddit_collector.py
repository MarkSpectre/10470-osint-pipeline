import praw, os 
from dotenv import load_dotenv 
load_dotenv() 
REDDIT_ID = os.getenv("REDDIT_ID") 
REDDIT_SECRET = os.getenv("REDDIT_SECRET") 
reddit = praw.Reddit(client_id=REDDIT_ID, 
 client_secret=REDDIT_SECRET, 
user_agent="osint_lab") 
def fetch_reddit(subreddit="technology", limit=20): 
    results = [] 
    for post in reddit.subreddit(subreddit).hot(limit=limit):  
        results.append({
        "platform": "reddit", 
        "user": str(post.author), 
        "timestamp": str(post.created_utc), 
        "text": post.title + " " + post.selftext,  "url": f"https://reddit.com{post.permalink}"  }) 
    return results 

