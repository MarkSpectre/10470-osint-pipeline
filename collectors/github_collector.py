import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="AI", limit=5):
    """Search GitHub repositories for the query and return repo entries as posts.

    This returns repository name + description as the `text` so the pipeline
    treats them as posts (instead of only returning user profiles with empty bios).
    """
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        # Search repositories (more likely to produce usable 'text' fields)
        res = requests.get(
            f"https://api.github.com/search/repositories",
            headers=headers,
            params={"q": query, "per_page": limit},
            timeout=10
        )
        res.raise_for_status()
        data = res.json()

        results = []
        for repo in data.get("items", [])[:limit]:
            owner = repo.get("owner", {}) or {}
            owner_login = owner.get("login", "")
            avatar = owner.get("avatar_url", "")
            repo_name = repo.get("name", "")
            repo_desc = repo.get("description") or ""
            html_url = repo.get("html_url", "")
            created_at = repo.get("created_at") or repo.get("updated_at") or ""

            results.append({
                "platform": "github",
                "user": owner_login,
                "username": owner_login,
                "name": repo_name,
                "email": "",
                "profile_pic": avatar,
                "timestamp": created_at,
                "text": repo_desc,
                "url": html_url
            })

        return results

    except Exception as e:
        print(f"GitHub error: {e}")
        return []
