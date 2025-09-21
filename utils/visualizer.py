import pandas as pd 
import matplotlib.pyplot as plt 
import sqlite3
from textblob import TextBlob

def plot_sentiment(db_path="data/osint.db"):
    conn = sqlite3.connect(db_path) 
    df = pd.read_sql("SELECT * FROM osint_data", conn) 
    conn.close() 
    df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)  
    df.groupby("platform")["sentiment"].mean().plot(kind="bar")  
    plt.title("Average Sentiment by Platform") 
    plt.show() 
