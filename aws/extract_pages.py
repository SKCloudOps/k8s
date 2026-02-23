
import re
import json

def extract_all_pages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by <div class="page">
    # Note: the first element will be everything before the first <div class="page">
    raw_pages = content.split('<div class="page">')[1:]
    
    pages_data = []
    for i, raw_page in enumerate(raw_pages):
        # Extract h2
        h2_match = re.search(r'<h2>(.*?)</h2>', raw_page)
        title = h2_match.group(1).strip() if h2_match else f"Page {i+1}"
        
        # Extract text content
        text_match = re.search(r'<div class="text">(.*?)</div>', raw_page, re.DOTALL)
        text_raw = text_match.group(1).strip() if text_match else ""
        # Clean text
        text_clean = re.sub(r'<br\s*/?>', '\n', text_raw)
        text_clean = re.sub(r'<.*?>', '', text_clean)
        text_clean = ' '.join(text_clean.split())
        
        # Extract img src
        img_match = re.search(r'<img.*?src="(.*?)".*?>', raw_page, re.DOTALL)
        img_src = img_match.group(1).strip() if img_match else ""
        
        pages_data.append({
            "id": i + 1,
            "title": title,
            "text": text_clean,
            "img": img_src
        })
    
    return pages_data

if __name__ == "__main__":
    file_path = r'c:\Sathish\rn_hw\k8s\aws\cloud_interview_guide_v7_full_embedded.html'
    data = extract_all_pages(file_path)
    
    # Just print the first 5 to verify
    for p in data[:5]:
        print(f"ID: {p['id']}, Title: {p['title']}, Text: {p['text'][:100]}...")
    
    # Save the titles and texts to a file for classification
    with open("pages_index.txt", "w", encoding='utf-8') as f:
        for p in data:
            f.write(f"ID: {p['id']} | Title: {p['title']} | Text: {p['text']}\n")
