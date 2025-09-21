# **OSINT Social Media Pipeline**

A comprehensive Open Source Intelligence (OSINT) pipeline for collecting, processing, and analyzing data from multiple social media platforms. This tool automatically gathers posts from various social networks, cleans and filters the data, performs sentiment analysis, and stores the results in a database for further analysis.


# **📋 Table of Contents**

Overview

Features

Supported Platforms

Installation

Configuration

Usage


# **🌟 Overview**

The OSINT Social Media Pipeline is designed for researchers, analysts, and security professionals who need to monitor and analyze content across multiple social media platforms simultaneously. The tool provides a unified interface to collect data from various sources, process it through a standardized pipeline, and output structured, analyzable data.


# **✨ Features**

Multi-Platform Support: Collect data from 10+ social media platforms

Data Cleaning: Automatic URL removal, symbol cleaning, and text normalization

Language Filtering: Filter content by language (English by default)

Sentiment Analysis: Automated sentiment scoring using TextBlob

Database Storage: SQLite database integration for persistent storage

Error Handling: Robust error handling and fallback mechanisms

Extensible Architecture: Easy to add new data sources and processing steps


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
