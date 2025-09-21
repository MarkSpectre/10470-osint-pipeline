import vk_api 
def fetch_vk(group_id="1", count=5): 
 vk_session = vk_api.VkApi(token="your_vk_token") 
 vk = vk_session.get_api() 
 posts = vk.wall.get(owner_id=-int(group_id), count=count)  
 results = [] 
 for p in posts["items"]: 
    results.append({ 
    "platform": "vk", 
    "user": str(p.get("from_id")), 
    "timestamp": str(p["date"]), 
    "text": p["text"], 
    "url": f"https://vk.com/wall{p['from_id']}_{p['id']}"  }) 
 return results
