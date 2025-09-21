from linkedin_api import Linkedin 
def fetch_linkedin(keyword="cybersecurity", limit=10):  
   api = Linkedin("your_email", "your_password") # best to use test  account 
   results = [] 
   people = api.search_people(keyword=keyword, limit=limit)  
   for p in people: 
    results.append({ 
    "platform": "linkedin", 
    "user": p.get("public_id", ""), 
    "timestamp": "N/A", 
    "text": p.get("headline", ""), 
    "url": f"https://linkedin.com/in/{p.get('public_id','')}"  }) 
    return results
