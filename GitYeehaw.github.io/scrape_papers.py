import requests
from bs4 import BeautifulSoup

URL = "https://arxiv.org/list/cs/new"  # Example source for CS papers

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

papers = soup.find_all('div', class_='list-title mathjax')

for paper in papers[:10]:  # Get latest 10 papers
    title = paper.text.replace("Title: ", "").strip()
    print(title)
