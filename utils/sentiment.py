# from textblob import TextBlob 

# def add_sentiment(records): 
#     if records is None:
#         return []
    
#     for r in records:
#         # Only add sentiment if text exists
#         if "text" in r and r["text"] is not None and isinstance(r["text"], str):
#             r["sentiment"] = TextBlob(r["text"]).sentiment.polarity
#         else:
#             r["sentiment"] = 0.0  # Default sentiment for records without text
    
#     return records

from textblob import TextBlob
import os
import matplotlib.pyplot as plt

def add_sentiment(data):
    """
    Adds a sentiment field to each record in the data list.
    Sentiment can be 'Positive', 'Negative', or 'Neutral'.
    """
    if not data:
        return []

    for record in data:
        text = record.get("text", "")
        if text:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1.0 to 1.0
            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
        else:
            sentiment = "Neutral"
        
        record["sentiment"] = sentiment

    return data

def save_sentiment_chart(data, output_dir="screenshots", filename="sentiment_chart.png"):
    """
    Creates a pie chart or bar chart of sentiment distribution and saves it as an image.
    """
    if not data:
        print("⚠️ No data to visualize.")
        return

    # Count sentiment types
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for record in data:
        s = record.get("sentiment", "Neutral")
        if s in counts:
            counts[s] += 1

    # Make sure folder exists
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Plot sentiment distribution
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140, colors=["#4CAF50", "#F44336", "#FFC107"])
    plt.title("Sentiment Distribution")

    # Save the chart
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"📊 Sentiment chart saved at: {filepath}")
