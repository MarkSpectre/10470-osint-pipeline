import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pathlib import Path
from textblob import TextBlob

def setup_dark_theme():
    """Set up dark theme for matplotlib"""
    plt.style.use('dark_background')
    sns.set_palette("husl")
    
def create_platform_stats_chart(db_path, output_path):
    """Create a visually appealing chart of platform statistics"""
    setup_dark_theme()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get platform counts
    cursor.execute("""
        SELECT platform, COUNT(*) as count 
        FROM social_media_posts 
        GROUP BY platform
        ORDER BY count DESC
    """)
    data = cursor.fetchall()
    platforms = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Create figure with transparent background
    plt.figure(figsize=(12, 6), facecolor='#121212')
    
    # Create bar plot with neon colors
    bars = plt.bar(platforms, counts, 
                   color=['#00ff9d', '#00ccff', '#ff00ff', '#ffff00'])
    
    # Customize the plot
    plt.title('Content Distribution Across Platforms', 
              color='#00ff9d', 
              fontsize=14, 
              pad=20)
    plt.xlabel('Platforms', color='#00ccff', fontsize=12)
    plt.ylabel('Number of Posts', color='#00ccff', fontsize=12)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', color='#00ff9d')

    # Customize grid
    plt.grid(True, alpha=0.1)
    
    # Add glow effect
    plt.gca().spines['bottom'].set_color('#00ccff')
    plt.gca().spines['top'].set_color('#00ccff')
    plt.gca().spines['left'].set_color('#00ccff')
    plt.gca().spines['right'].set_color('#00ccff')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path, 
                bbox_inches='tight',
                facecolor='#121212',
                edgecolor='none',
                dpi=300)
    plt.close()

def plot_sentiment(db_path, output_path):
    """Create sentiment analysis visualization"""
    setup_dark_theme()
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("""
        SELECT platform, text, sentiment 
        FROM social_media_posts 
        WHERE sentiment IS NOT NULL
    """, conn)
    conn.close()

    plt.figure(figsize=(12, 6), facecolor='#121212')
    
    # Create grouped bar plot for sentiment
    platforms = df.platform.unique()
    sentiments = ['Positive', 'Neutral', 'Negative']
    
    data = []
    for platform in platforms:
        platform_data = df[df.platform == platform]
        pos = (platform_data.sentiment > 0.2).mean()
        neu = ((platform_data.sentiment >= -0.2) & (platform_data.sentiment <= 0.2)).mean()
        neg = (platform_data.sentiment < -0.2).mean()
        data.append([pos, neu, neg])
    
    x = range(len(platforms))
    width = 0.25
    
    # Plot bars with neon colors
    plt.bar([i - width for i in x], [d[0] for d in data], width, 
            label='Positive', color='#00ff9d', alpha=0.8)
    plt.bar([i for i in x], [d[1] for d in data], width,
            label='Neutral', color='#00ccff', alpha=0.8)
    plt.bar([i + width for i in x], [d[2] for d in data], width,
            label='Negative', color='#ff00ff', alpha=0.8)
    
    plt.title('Sentiment Distribution by Platform',
              color='#00ff9d',
              fontsize=14,
              pad=20)
    plt.xlabel('Platform', color='#00ccff', fontsize=12)
    plt.ylabel('Proportion', color='#00ccff', fontsize=12)
    plt.xticks(range(len(platforms)), platforms, rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    
    # Add legend with custom colors
    plt.legend(facecolor='#121212', edgecolor='#00ccff', labelcolor='white')
    
    # Add glow effect
    plt.gca().spines['bottom'].set_color('#00ccff')
    plt.gca().spines['top'].set_color('#00ccff')
    plt.gca().spines['left'].set_color('#00ccff')
    plt.gca().spines['right'].set_color('#00ccff')
    
    plt.grid(True, alpha=0.1)
    plt.tight_layout()
    
    plt.savefig(output_path,
                bbox_inches='tight',
                facecolor='#121212',
                edgecolor='none',
                dpi=300)
    plt.close()
