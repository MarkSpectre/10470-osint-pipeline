# **OSINT Social Media Pipeline**

A comprehensive Open Source Intelligence (OSINT) pipeline for collecting, processing, and analyzing data from multiple social media platforms. This tool automatically gathers posts from various social networks, cleans and filters the data, performs sentiment analysis, and stores the results in a database for further analysis.


# **📋 Table of Contents**

- [Overview](#overview)
- [Features](#features)
- [API Keys Setup](#api-keys-setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

# **🔑 API Keys Setup**

To use all features of the OSINT pipeline, you'll need to set up the following API keys:

1. **RapidAPI Key** (Required)
   - Used for: Twitter, Instagram, TikTok, Facebook
   - Get it from: [RapidAPI](https://rapidapi.com/)
   - Set as: `RAPIDAPI_KEY` in .env

2. **GitHub Personal Access Token**
   - Used for: GitHub data collection
   - Get it from: [GitHub Developer Settings](https://github.com/settings/tokens)
   - Set as: `GITHUB_TOKEN` in .env

3. **Twitter Bearer Token**
   - Used for: Twitter API v2 (fallback)
   - Get it from: [Twitter Developer Portal](https://developer.twitter.com/)
   - Set as: `TWITTER_BEARER_TOKEN` in .env

4. **Reddit API Credentials**
   - Used for: Reddit data collection
   - Get it from: [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Set as: `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` in .env

5. **Mastodon Access Token**
   - Used for: Mastodon instance access
   - Get it from your Mastodon instance
   - Set as: `MASTODON_ACCESS_TOKEN` in .env

Create a `.env` file in the root directory with your API keys:

```env
# RapidAPI (Required)
RAPIDAPI_KEY="your_rapidapi_key_here"

# Platform-specific APIs
GITHUB_TOKEN="your_github_token_here"
TWITTER_BEARER_TOKEN="your_twitter_bearer_token_here"
REDDIT_CLIENT_ID="your_reddit_client_id_here"
REDDIT_CLIENT_SECRET="your_reddit_secret_here"
MASTODON_ACCESS_TOKEN="your_mastodon_token_here"
```


# **🌟 Overview**

The OSINT Social Media Pipeline is designed for researchers, analysts, and security professionals who need to monitor and analyze content across multiple social media platforms simultaneously. The tool provides a unified interface to collect data from various sources, process it through a standardized pipeline, and output structured, analyzable data.


# **✨ Features**

- **Multi-Platform Data Collection**
  - Seamless integration with 10+ social media platforms
  - Unified data collection interface
  - Rate limit handling and API fallbacks

- **Advanced Data Processing**
  - Automatic URL removal and text normalization
  - Language detection and filtering
  - Sentiment analysis with TextBlob
  - User data enrichment from multiple sources

- **Modern Web Interface**
  - Dark theme with neon accents
  - Real-time data visualization
  - Interactive dashboards
  - Responsive design for all devices

- **Robust Architecture**
  - SQLite database for persistent storage
  - Comprehensive error handling
  - Extensible collector system
  - API key management and validation

- **Data Analysis**
  - Cross-platform user tracking
  - Sentiment visualization
  - Platform usage statistics
  - Content trend analysis

- **User Experience**
  - Advanced search capabilities
  - Platform-specific filtering
  - Data export options
  - Real-time updates


# **📱 Supported Platforms**

✅ Twitter (via RapidAPI)

✅ Reddit (via PRAW)

✅ Facebook (via Graph API/RapidAPI)

✅ Instagram (via Instagrapi)

✅ TikTok (via RapidAPI)

✅ Mastodon (via Mastodon.py)

✅ GitHub (via GitHub API)

✅ Snapchat (via RapidAPI)


# **🔧 Installation**

Prerequisites
Python 3.8+

pip (Python package manager)

API keys for various services (see Configuration)

Step-by-Step Installation
1.Clone the repository
git clone https://github.com/yourusername/osint-pipeline.git
cd osint-pipeline

2.Create a virtual environment
python -m venv osint_env
source osint_env/bin/activate  # On Windows: osint_env\Scripts\activate

3.Install dependencies
pip install -r requirements.txt


# **⚙️ Configuration**
Environment Variables
Create a .env file in the root directory with the following variables:

## **RapidAPI Keys**

TIKTOK_KEY=your_tiktok_api_key_here

SNAPCHAT_KEY=your_snapchat_api_key_here

FACEBOOK_ACCESS_TOKEN=your_facebook_key_here

INSTAGRAM_KEY=your_instagram_key_here

TWITTER_KEY=your_twitter_key_here

## **Reddit API**

REDDIT_CLIENT_ID=your_reddit_client_id

REDDIT_CLIENT_SECRET=your_reddit_client_secret

REDDIT_USER_AGENT=your_reddit_user_agent

## **GitHub API**

GITHUB_TOKEN=your_github_token_here

## **Mastodon API**

MATODON_TOKEN=your_mastodon_token_here


# **🚀 Usage**

Run the complete pipeline:

python main.py
