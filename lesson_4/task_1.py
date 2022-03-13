"""1. Написать приложение, которое собирает основные новости с сайтов
https://news.mail.ru,
https://lenta.ru,
https://yandex.ru/news.
Для парсинга использовать XPath. Структура данных должна содержать:
 название источника;
 наименование новости;
 ссылку на новость;
 дата публикации.
 2. Сложить собранные новости в БД
 """

import requests
from lxml import html
from pymongo import MongoClient


def get_news_from_lenta(url, headers):
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    data = dom.xpath("//a[@class='card-big _topnews _news' or @class = 'card-mini _topnews']")
    news_list = []

    for news in data:
        news_dict = {}
        news_portal = url
        info = news.xpath(".//h3/text() | .//span[@class='card-mini__title']/text()")[0]
        link = news.xpath("./@href")[0]
        date = news.xpath(".//time/text()")[0]

        news_dict['news_portal'] = news_portal
        news_dict['name'] = info
        news_dict['link'] = link
        news_dict['date'] = f'{date}'

        news_list.append(news_dict)
    return news_list


def fill_db(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news_db']
    news_lenta = db.lenta_news
    for item in data:
        if news_lenta.count_documents({'link': item['link']}) == 0:
            news_lenta.insert_one(item)


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/98.0.4758.82 Safari/537.36'}
    url = 'https://lenta.ru/'
    print(get_news_from_lenta(url, header))
    fill_db(get_news_from_lenta(url, header))
