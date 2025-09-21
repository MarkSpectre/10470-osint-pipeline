import requests 
from bs4 import BeautifulSoup 
def fetch_quora(query="osint", limit=5): 
 url = f"https://www.quora.com/search?q={query}"  
 soup = BeautifulSoup(requests.get(url).text, "html.parser")
 results = [] 
 for i, q in enumerate(soup.find_all("span", {"class": "q-text"})):  
    if i >= limit: 
        break 
    results.append({ 
        "platform": "quora", 
        "user": "anonymous", 
        "timestamp": "N/A", 
        "text": q.get_text(), 
        "url": url 
        }) 
 return results 
