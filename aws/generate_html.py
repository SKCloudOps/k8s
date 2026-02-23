
import re
import json
import os

def extract_all_pages(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by <div class="page">
    parts = content.split('<div class="page">')[1:]
    
    pages_data = []
    for i, raw_page in enumerate(parts):
        # We need to find where the page ends. Usually there's a trailing </div> for the page itself.
        # But we can just search within the part until the next page or end of file.
        
        # Extract title from h2
        h2_match = re.search(r'<h2>(.*?)</h2>', raw_page)
        title = h2_match.group(1).strip() if h2_match else f"Page {i+1}"
        
        # Extract text from <div class="text">
        text_match = re.search(r'<div class="text">(.*?)</div>', raw_page, re.DOTALL)
        text_raw = text_match.group(1).strip() if text_match else ""
        
        # Clean up text
        text_clean = re.sub(r'<br\s*/?>', '\n', text_raw)
        text_clean = re.sub(r'<.*?>', '', text_clean)
        text_clean = ' '.join(text_clean.split())
        
        # Extract image src
        img_match = re.search(r'<img.*?src="(.*?)".*?>', raw_page, re.DOTALL)
        img_src = img_match.group(1).strip() if img_match else ""
        
        pages_data.append({
            "id": i + 1,
            "title": title,
            "text": text_clean,
            "img": img_src
        })
    return pages_data

mapping = {
    1: None, # ToC
    2: "compute",
    3: "networking",
    4: "serverless",
    5: "serverless",
    6: "serverless",
    7: "compute",
    8: "networking",
    9: "cost",
    10: "storage",
    11: "networking",
    12: "devops",
    13: "devops",
    14: "compute",
    15: "devops",
    16: "devops",
    17: "compute",
    18: "compute",
    19: "analytics",
    20: "analytics",
    21: "analytics",
    22: "compute",
    23: "compute",
    24: "devops",
    25: "analytics",
    26: "devops",
    27: "security",
    28: "networking",
    29: "security",
    30: "devops",
    31: "networking",
    32: "compute",
    33: "compute",
    34: "devops",
    35: "networking",
    36: "cost",
    37: "security",
    38: "serverless",
    39: "serverless",
    40: "serverless",
    41: "compute",
    42: "database",
    43: "storage",
    44: "compute",
    45: "compute",
    46: "compute",
    47: "compute",
    48: "compute",
    49: "cost",
    50: "serverless",
    51: "compute",
    52: "serverless",
    53: "compute",
    54: "networking",
    55: "networking",
}

def generate_sections(data):
    sections = {
        "compute": [],
        "networking": [],
        "storage": [],
        "database": [],
        "security": [],
        "devops": [],
        "serverless": [],
        "analytics": [],
        "cost": []
    }
    
    for p in data:
        sec = mapping.get(p["id"])
        if sec:
            safe_title = p['title'].replace("'", "\\'")
            html = f"""
                <div class="resource-card" data-id="{p['id']}">
                    <div class="resource-image" onclick="openModal('{p['img']}', '{safe_title}')">
                        <img src="{p['img']}" alt="{p['title']}">
                    </div>
                    <div class="resource-info">
                        <h3>{p['title']}</h3>
                        <p class="short-text">{p['text'][:240]}...</p>
                        <div class="full-text" style="display:none;">{p['text']}</div>
                        <button class="expand-btn" onclick="toggleResource(this)">Read More</button>
                    </div>
                </div>
            """
            sections[sec].append(html)
            
    return sections

if __name__ == "__main__":
    file_path = r'c:\Sathish\rn_hw\k8s\aws\cloud_interview_guide_v7_full_embedded.html'
    data = extract_all_pages(file_path)
    print(f"Extracted {len(data)} pages.")
    
    sections_html = generate_sections(data)
    
    output_path = r'c:\Sathish\rn_hw\k8s\aws\generated_content.json'
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(sections_html, f, indent=2)
    print(f"Generated content saved to {output_path}")
