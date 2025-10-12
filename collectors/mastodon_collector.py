from mastodon import Mastodon

mastodon = Mastodon(
    access_token="YOUR_ACCESS_TOKEN",
    api_base_url="https://mastodon.social"
)

def fetch_mastodon(hashtag="osint", limit=10):
    results = []
    posts = mastodon.timeline_hashtag(hashtag, limit=limit)
    for p in posts:
        user = p.get("account", {})
        results.append({
            "platform": "mastodon",
            "name": user.get("display_name", ""),
            "username": user.get("username", ""),
            "email": "",
            "profile_pic": user.get("avatar", ""),
            "timestamp": str(p.get("created_at", "")),
            "text": p.get("content", ""),
            "url": p.get("url", "")
        })
    return results
