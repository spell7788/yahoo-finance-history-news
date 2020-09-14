import csv
import pathlib
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Comment, NavigableString

_YAHOO_FINANCE_BASE = 'https://finance.yahoo.com'
_NEWS_BASE_URL = f'{_YAHOO_FINANCE_BASE}/quote/{{company}}'

def get_news_html(company: str) -> str:
    resp = requests.get(_NEWS_BASE_URL.format(company=company))
    return resp.text


def is_news_link(href: str) -> bool:
    return (
        href != '/news/'
        and href != '/m/'
        and (href.startswith('/news/') or href.startswith('/m/'))
    )


def get_news_links(html: str) -> list:
    soup = BeautifulSoup(html, features='html.parser')
    links = []
    for link in soup('a', href=is_news_link):
        try:
            title = next(
                child
                for child in link.children
                if isinstance(child, NavigableString) and not isinstance(child, Comment)
            )
        except StopIteration:
            continue

        links.append((title, link['href']))

    return links


def save_news_links(filepath: pathlib.Path, links: list) -> None:
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['title', 'link'])
        for title, link in links:
            writer.writerow([title, urljoin(_YAHOO_FINANCE_BASE, link)])
