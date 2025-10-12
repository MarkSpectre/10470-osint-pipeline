import snscrape.modules.twitter as sntwitter 
def fetch_twitter_scrape(query="OSINT", limit=10): 
 results = [] 
 for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):  
    if i >= limit: 
        break 
    results.append({
        "platform": "twitter",
        "user": tweet.user.username,
        "username": tweet.user.username,
        "name": tweet.user.displayname if hasattr(tweet.user, "displayname") else "",
        "email": "",
        "profile_pic": tweet.user.profileImageUrl if hasattr(tweet.user, "profileImageUrl") else "",
        "timestamp": str(tweet.date),
        "text": tweet.content,
        "url": tweet.url
    })
 return results 
