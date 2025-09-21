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

