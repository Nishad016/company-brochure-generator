from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_website_contents(url):
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string if soup.title else "No title found"

    if soup.body:
        for item in soup.body(["script", "style", "img", "input"]):
            item.decompose()

        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""

    return (title + "\n\n" + text)[:2000]


def fetch_website_links(url):
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []

    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        links.append(full_url)

    return list(set(links))
