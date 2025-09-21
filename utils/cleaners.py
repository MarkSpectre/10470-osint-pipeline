from langdetect import detect, DetectorFactory
import re 

# Set seed for consistent results
DetectorFactory.seed = 0

def clean_text(text): 
    if text is None:
        return ""
    text = re.sub(r"http\S+", "", text)  # remove URLs 
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove symbols  
    return text.strip()

def filter_english(records):
    """
    Filter records to only include English content with comprehensive error handling
    """
    if records is None:
        return []
    
    results = []
    
    for r in records:
        # Skip if record doesn't have a text field or text is None
        if "text" not in r or r["text"] is None:
            continue
            
        text = r["text"]
        
        # Convert to string if it's not already
        if not isinstance(text, str):
            try:
                text = str(text)
            except:
                continue
                
        # Skip empty strings
        if not text.strip():
            continue
            
        try:
            # Try to detect language
            lang = detect(text)
            if lang == "en":
                results.append(r)
        except Exception as e:
            # Skip records where language detection fails
            print(f"Language detection failed for text: {text[:100]}... Error: {e}")
            continue
            
    return results