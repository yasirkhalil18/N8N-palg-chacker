import requests
from bs4 import BeautifulSoup
import hashlib

def check_plagiarism(text):
    query = '+'.join(text.split()[:8])
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        return {'error': 'Failed to fetch search results', 'details': str(e)}

    if response.status_code != 200:
        return {'error': 'Google search failed', 'status_code': response.status_code}

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a')

    hashes = []
    for link in results[:3]:
        href = link.get('href')
        if href and 'http' in href:
            try:
                page = requests.get(href, timeout=5)
                content = BeautifulSoup(page.text, 'html.parser').get_text()
                page_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                hashes.append(page_hash)
            except:
                continue

    original_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    match_count = hashes.count(original_hash)
    percent = (match_count / len(hashes)) * 100 if hashes else 0.0

    return {'plag_percent': round(percent, 2)}
