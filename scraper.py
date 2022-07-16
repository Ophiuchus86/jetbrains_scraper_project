import string

import bs4.element
import requests
import os
from bs4 import BeautifulSoup

HEADERS = {'Accept-Language': 'en-US,en;q=0.5'}
URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
saved_articles = []


def find_articles_links(response: requests.Response, articles_type: str):
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("li", {"class": "app-article-list-row__item"})

    matched_articles = []
    for article in articles:
        if article.find("span", {"class": "c-meta__type"}).text == articles_type:
            matched_articles.append(article.find("a", {"class": "c-card__link"}))

    return matched_articles


def save_content(a: bs4.element.Tag, folder: str):
    r = requests.get("https://www.nature.com" + a.attrs["href"])
    soup = BeautifulSoup(r.content, "html.parser")
    body = soup.find("div", {"class": "c-article-body"})
    filename = get_proper_filename(a.getText())
    with open(os.path.join(folder, filename), "wb") as file:
        file.write(body.text.strip().encode("utf-8"))
    saved_articles.append(filename)


def get_proper_filename(filename: str):
    for ch in filename:
        if ch in string.punctuation:
            filename = filename.replace(ch, "")
    return "_".join(filename.split()) + ".txt"


def main():
    n_pages = int(input())
    articles_type = input()
    for page in range(1, n_pages + 1):
        folder = f"Page_{page}"
        if not os.path.exists(folder):
            os.mkdir(folder)

        response = requests.get(URL + f"&page={page}", headers=HEADERS)
        for link in find_articles_links(response, articles_type):
            save_content(link, folder)

    print("Saved articles:\n", saved_articles)


if __name__ == "__main__":
    main()
