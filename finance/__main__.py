import sys
from pathlib import Path

from .history import download_history, save_history
from .news import get_news_html, get_news_links, save_news_links

if __name__ == '__main__':
    data_folder = Path('./data')

    for company in sys.argv[1:]:
        csv_ = download_history(company)
        filepath = data_folder / f'{company}.csv'
        save_history(filepath, csv_)

        news_html = get_news_html(company)
        news_links = get_news_links(news_html)
        filepath = data_folder / f'{company}_news.csv'
        save_news_links(filepath, news_links)
