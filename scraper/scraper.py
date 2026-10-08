import requests
from bs4 import BeautifulSoup

URL = 'https://books.toscrape.com/'

response = requests.get(URL,timeout=10)

response.raise_for_status()

soup = BeautifulSoup(response.text,"html.parser")


print(soup.get_text(strip=True))