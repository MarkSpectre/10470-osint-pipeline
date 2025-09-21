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
