import requests
from bs4 import BeautifulSoup
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=HEADERS)
    time.sleep(1.5)  # Avoid being blocked
    return response.text

def extract_results(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    return [res.get_text() for res in results if res.get_text()]

def clean_sentence(sentence):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    return sentence.strip().lower()

def check_text(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    total = len(sentences)
    plagiarized = 0

    for sentence in sentences:
        clean = clean_sentence(sentence)
        if not clean or len(clean) < 8:
            continue

        html = search_google(f'"{clean}"')  # Exact match
        results = extract_results(html)
        found = any(clean in result.lower() for result in results)

        if found:
            plagiarized += 1

    if total == 0:
        return 0.0

    return round((plagiarized / total) * 100, 2)
