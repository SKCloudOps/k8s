
import re

def extract_pages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find <div class="page"> blocks
    page_blocks = re.findall(r'<div class="page">.*?<img.*?src="(.*?)".*?</div>', content, re.DOTALL)
    
    # But I want the text and h2 too
    pages = re.findall(r'<div class="page">(.*?)</div>', content, re.DOTALL)
    
    summaries = []
    for page in pages:
        h2_match = re.search(r'<h2>(.*?)</h2>', page)
        page_num = h2_match.group(1).strip() if h2_match else "Unknown"
        
        text_match = re.search(r'<div class="text">(.*?)</div>', page, re.DOTALL)
        text_content = text_match.group(1).strip() if text_match else ""
        # Remove HTML tags from text
        text_content = re.sub(r'<.*?>', ' ', text_content)
        text_content = ' '.join(text_content.split())
        
        summaries.append(f"{page_num}: {text_content[:200]}...")
    
    return summaries

if __name__ == "__main__":
    file_path = r'c:\Sathish\rn_hw\k8s\aws\cloud_interview_guide_v7_full_embedded.html'
    summaries = extract_pages(file_path)
    for s in summaries:
        print(s)
