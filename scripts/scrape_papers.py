import requests
from bs4 import BeautifulSoup
import os
import re

BASE_URL = "https://arxiv.org"
LIST_URL = "https://arxiv.org/list/cs/new"

pdf_dir = "papers"  # Assuming directory already exists

response = requests.get(LIST_URL)
soup = BeautifulSoup(response.text, 'html.parser')

entries = soup.find_all('dt')
titles = soup.find_all('div', class_='list-title mathjax')

for i, (entry, title) in enumerate(zip(entries, titles)):
    if i >= 10:
        break

    pdf_link_tag = entry.find('a', title="Download PDF")
    if pdf_link_tag:
        pdf_url = BASE_URL + pdf_link_tag['href']
        paper_title = title.text.replace("Title:", "").strip()

        # Robust filename sanitization (remove problematic chars)
        clean_title = re.sub(r'[^A-Za-z0-9 ]+', '', paper_title).replace(' ', '_')
        filename = f"{clean_title[:100]}.pdf"
        filepath = os.path.join(pdf_dir, filename)

        print(f"Downloading: {paper_title}")
        pdf_response = requests.get(pdf_url)

        # Save PDF file
        with open(filepath, 'wb') as f:
            f.write(pdf_response.content)

print("All PDFs downloaded successfully.")
