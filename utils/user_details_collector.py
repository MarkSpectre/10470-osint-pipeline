"""
Enhanced user details collector supporting both RapidAPI and official APIs.
Provides consistent interface for collecting user information from multiple social platforms.
"""
import os
import time
from typing import Dict, Any
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from dotenv import load_dotenv

load_dotenv()

# API Keys
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_KEY")
INSTAGRAM_KEY = os.getenv("INSTAGRAM_KEY")
INSTAGRAM_HOST = os.getenv("INSTAGRAM_HOST", "instagram-scraper-2022.p.rapidapi.com")
FACEBOOK_KEY = os.getenv("FACEBOOK_KEY")
FACEBOOK_HOST = os.getenv("FACEBOOK_RAPID_HOST", "facebook-profile-data.p.rapidapi.com")
TIKTOK_KEY = os.getenv("TIKTOK_KEY")

# Configure retry strategy
retry_strategy = Retry(
    total=3,  # number of retries
    status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
    allowed_methods=["GET"],  # HTTP methods to retry
    backoff_factor=1  # wait 1, 2, 4 seconds between retries
)

# Create session with retry strategy
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

def get_github_user_details(username: str) -> dict:
    """
    Fetch detailed user information from GitHub API
    
    Args:
        username (str): GitHub username to fetch details for
        
    Returns:
        dict: Dictionary containing user details or empty dict if failed
    """
    if not username:
        return {}

    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    try:
        response = requests.get(
            f"https://api.github.com/users/{username}", 
            headers=headers,
            timeout=10
        )
        # Handle rate limiting
        if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
            print(f"GitHub API rate limit exceeded. Reset at: {response.headers['X-RateLimit-Reset']}")
            return {}
            
        if response.status_code == 200:
            data = response.json()
            return {
                "platform": "github",
                "username": data.get("login", ""),
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "profile_pic": data.get("avatar_url", ""),
                "bio": data.get("bio", ""),
                "location": data.get("location", ""),
                "followers": data.get("followers", 0),
                "following": data.get("following", 0),
                "company": data.get("company", ""),
                "blog": data.get("blog", ""),
                "public_repos": data.get("public_repos", 0),
                "public_gists": data.get("public_gists", 0),
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", "")
            }
        else:
            print(f"GitHub API error: {response.status_code} - {response.text}")
    except requests.Timeout:
        print(f"Timeout while fetching GitHub user details for {username}")
    except requests.RequestException as e:
        print(f"Network error while fetching GitHub user details: {e}")
    except Exception as e:
        print(f"Error fetching GitHub user details: {e}")
    return {}

def get_twitter_user_details(username: str) -> dict:
    """
    Fetch Twitter user details using RapidAPI
    
    Args:
        username (str): Twitter username to fetch details for
        
    Returns:
        dict: Dictionary containing user details or empty dict if failed
    """
    if not username or not RAPIDAPI_KEY:
        return {}

    url = "https://twitter154.p.rapidapi.com/user/details"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }
    params = {"username": username}

    try:
        # Add timeout to prevent hanging
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        # Handle rate limiting
        if response.status_code == 429:
            print("Twitter RapidAPI rate limit exceeded")
            return {}
            
        if response.status_code == 200:
            data = response.json()
            return {
                "platform": "twitter",
                "username": data.get("username", ""),
                "name": data.get("name", ""),
                "email": "",  # Twitter API doesn't provide email
                "profile_pic": data.get("profile_pic_url", ""),
                "bio": data.get("description", ""),
                "location": data.get("location", ""),
                "followers": data.get("followers_count", 0),
                "following": data.get("following_count", 0),
                "verified": data.get("verified", False),
                "created_at": data.get("creation_date", ""),
                "tweets_count": data.get("number_of_tweets", 0),
                "likes_count": data.get("number_of_likes", 0)
            }
        else:
            print(f"Twitter API error: {response.status_code} - {response.text}")
    except requests.Timeout:
        print(f"Timeout while fetching Twitter user details for {username}")
    except requests.RequestException as e:
        print(f"Network error while fetching Twitter user details: {e}")
    except Exception as e:
        print(f"Error fetching Twitter user details: {e}")
    return {}

def get_instagram_user_details(username: str) -> dict:
    """
    Fetch Instagram user details using RapidAPI
    
    Args:
        username (str): Instagram username to fetch details for
        
    Returns:
        dict: Dictionary containing user details or empty dict if failed
    """
    if not username or not RAPIDAPI_KEY:
        return {}

    url = f"https://{INSTAGRAM_HOST}/ig/info_username"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": INSTAGRAM_HOST
    }
    params = {"user": username}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        # Handle rate limiting
        if response.status_code == 429:
            print("Instagram RapidAPI rate limit exceeded")
            return {}
            
        if response.status_code == 200:
            data = response.json().get("user", {})
            return {
                "platform": "instagram",
                "username": data.get("username", ""),
                "name": data.get("full_name", ""),
                "email": "",
                "profile_pic": data.get("profile_pic_url_hd", ""),
                "bio": data.get("biography", ""),
                "location": "",
                "followers": data.get("follower_count", 0),
                "following": data.get("following_count", 0),
                "is_private": data.get("is_private", False),
                "is_verified": data.get("is_verified", False),
                "posts_count": data.get("media_count", 0),
                "external_url": data.get("external_url", "")
            }
        else:
            print(f"Instagram API error: {response.status_code} - {response.text}")
    except requests.Timeout:
        print(f"Timeout while fetching Instagram user details for {username}")
    except requests.RequestException as e:
        print(f"Network error while fetching Instagram user details: {e}")
    except Exception as e:
        print(f"Error fetching Instagram user details: {e}")
    return {}

def get_facebook_user_details(username):
    """Fetch Facebook user details using RapidAPI"""
    if not username or not RAPIDAPI_KEY:
        return {}

    url = f"https://{FACEBOOK_HOST}/profile"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": FACEBOOK_HOST
    }
    params = {"username": username}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                "platform": "facebook",
                "username": username,
                "name": data.get("name", ""),
                "email": "",
                "profile_pic": data.get("profile_pic", ""),
                "bio": data.get("about", ""),
                "location": data.get("location", ""),
                "followers": data.get("followers_count", 0),
                "following": 0  # Facebook API doesn't provide following count
            }
    except Exception as e:
        print(f"Error fetching Facebook user details: {e}")
    return {}

def get_tiktok_user_details(username):
    """Fetch TikTok user details using RapidAPI"""
    if not username or not RAPIDAPI_KEY:
        return {}

    url = "https://tiktok-api6.p.rapidapi.com/user/info"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "tiktok-api6.p.rapidapi.com"
    }
    params = {"unique_id": username}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("user", {})
            return {
                "platform": "tiktok",
                "username": username,
                "name": data.get("nickname", ""),
                "email": "",
                "profile_pic": data.get("avatarLarger", ""),
                "bio": data.get("signature", ""),
                "location": "",
                "followers": data.get("followerCount", 0),
                "following": data.get("followingCount", 0)
            }
    except Exception as e:
        print(f"Error fetching TikTok user details: {e}")
    return {}

def get_reddit_user_details(username):
    """Fetch Reddit user details using official API"""
    if not username:
        return {}

    try:
        response = requests.get(f"https://www.reddit.com/user/{username}/about.json",
                              headers={'User-Agent': 'OSINT_Pipeline/1.0'})
        if response.status_code == 200:
            data = response.json().get("data", {})
            return {
                "platform": "reddit",
                "username": username,
                "name": "",  # Reddit API doesn't provide real names
                "email": "",
                "profile_pic": data.get("icon_img", "").split('?')[0],
                "bio": data.get("subreddit", {}).get("public_description", ""),
                "location": "",
                "followers": data.get("subscribers", 0),
                "following": 0  # Reddit API doesn't provide following count
            }
    except Exception as e:
        print(f"Error fetching Reddit user details: {e}")
    return {}

def get_mastodon_user_details(username):
    """Fetch Mastodon user details using official API"""
    if not username:
        return {}

    try:
        from mastodon import Mastodon
        mastodon = Mastodon(
            access_token=os.getenv("MASTODON_ACCESS_TOKEN"),
            api_base_url="https://mastodon.social"
        )
        data = mastodon.account_lookup(username)
        return {
            "platform": "mastodon",
            "username": data.get("username", ""),
            "name": data.get("display_name", ""),
            "email": "",
            "profile_pic": data.get("avatar", ""),
            "bio": data.get("note", ""),
            "location": "",
            "followers": data.get("followers_count", 0),
            "following": data.get("following_count", 0)
        }
    except Exception as e:
        print(f"Error fetching Mastodon user details: {e}")
    return {}

def enrich_user_data(platform: str, username: str) -> Dict[str, Any]:
    """
    Get enriched user data based on platform and username
    
    Args:
        platform (str): Social media platform name (e.g., 'twitter', 'github')
        username (str): Username on the specified platform
        
    Returns:
        Dict[str, Any]: Dictionary containing user details with consistent fields:
            - platform: str
            - username: str
            - name: str
            - email: str
            - profile_pic: str
            - bio: str
            - location: str
            - followers: int
            - following: int
            - last_updated: str (ISO format timestamp)
            Additional platform-specific fields may be included
    """
    platform = platform.lower().strip()
    if not username or not platform:
        return create_empty_user_data(platform, username)

    # Map platforms to their respective detail fetcher functions
    platform_functions = {
        'twitter': get_twitter_user_details,
        'instagram': get_instagram_user_details,
        'facebook': get_facebook_user_details,
        'tiktok': get_tiktok_user_details,
        'github': get_github_user_details,
        'reddit': get_reddit_user_details,
        'mastodon': get_mastodon_user_details
    }

    # Get the appropriate function and fetch user details
    fetch_func = platform_functions.get(platform)
    if not fetch_func:
        print(f"Unsupported platform: {platform}")
        return create_empty_user_data(platform, username)

    try:
        user_data = fetch_func(username)
        if user_data:
            # Ensure consistent platform field
            user_data["platform"] = platform
            user_data["last_updated"] = datetime.now().isoformat()
            return user_data
        else:
            print(f"No data found for {username} on {platform}")
    except Exception as e:
        print(f"Error enriching user data for {username} on {platform}: {e}")

    return create_empty_user_data(platform, username)

def create_empty_user_data(platform: str, username: str) -> Dict[str, Any]:
    """
    Create an empty user data dictionary with default values
    
    Args:
        platform (str): Social media platform name
        username (str): Username on the platform
        
    Returns:
        Dict[str, Any]: Dictionary with default user data fields
    """
    return {
        "platform": platform,
        "username": username,
        "name": "",
        "email": "",
        "profile_pic": "",
        "bio": "",
        "location": "",
        "followers": 0,
        "following": 0,
        "last_updated": datetime.now().isoformat()
    }