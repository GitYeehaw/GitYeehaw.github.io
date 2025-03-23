import requests
from bs4 import BeautifulSoup
import os

# URL of the latest Computer Science papers
BASE_URL = "https://arxiv.org"
LIST_URL = "https://arxiv.org/list/cs/new"

pdf_dir = "papers"  # assuming this directory already exists

# Get webpage content
response = requests.get(LIST_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Find paper entries
entries = soup.find_all('dt')
titles = soup.find_all('div', class_='list-title mathjax')

# Download and save PDFs
for i, (entry, title) in enumerate(zip(entries, titles)):
    if i >= 10:
        break  # Limit to 10 papers

    pdf_link_tag = entry.find('a', title="Download PDF")
    if pdf_link_tag:
        pdf_url = BASE_URL + pdf_link_tag['href']
        paper_title = title.text.replace("Title: ", "").strip()

        # Sanitize filename
        filename = f"{paper_title[:100].replace(' ', '_').replace('/', '_')}.pdf"
        filepath = os.path.join(pdf_dir, filename)

        print(f"Downloading: {paper_title}")
        pdf_response = requests.get(pdf_url)

        # Save PDF file
        with open(filepath, 'wb') as f:
            f.write(pdf_response.content)

print("All PDFs downloaded successfully.")
