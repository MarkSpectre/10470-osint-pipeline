from textblob import TextBlob 

def add_sentiment(records): 
    if records is None:
        return []
    
    for r in records:
        # Only add sentiment if text exists
        if "text" in r and r["text"] is not None and isinstance(r["text"], str):
            r["sentiment"] = TextBlob(r["text"]).sentiment.polarity
        else:
            r["sentiment"] = 0.0  # Default sentiment for records without text
    
    return records