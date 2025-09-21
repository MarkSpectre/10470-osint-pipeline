import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="leak", limit=5):
    """
    Fetch GitHub repositories using GitHub REST API
    """
    try:
        headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Add authorization if token is available
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        # Search repositories
        url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"GitHub API Error: HTTP {response.status_code}")
            return []
        
        data = response.json()
        results = []
        
        # Extract repositories from the response
        for repo in data.get('items', [])[:limit]:
            results.append({
                "platform": "github",
                "user": repo['owner']['login'],
                "timestamp": repo['created_at'],
                "text": f"{repo['name']}: {repo['description']}" if repo['description'] else repo['name'],
                "url": repo['html_url']
            })
            
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub data: {e}")
        return []