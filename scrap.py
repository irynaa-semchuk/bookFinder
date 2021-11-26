# coding: cp1251
import re
from urllib.request import urlopen, Request
from urllib.parse import quote, quote_plus
from bs4 import BeautifulSoup as bs
from math import inf

TRANSLITERATION = {' ': '-', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
                   'є': 'je', 'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'й': 'j', 'к': 'k',
                   'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
                   'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh',
                   'щ': 'sch', 'ю': 'ju', 'я': 'ja', 'ь': '', }


def translit(s):
    res = ''
    for item in s:
        res += TRANSLITERATION[item.lower()]
    return res


def get_price(author, title, site):
    if site == 'bambook.com':
        query = quote_plus(title, encoding="windows-1251")
        url = f"https://{site}/scripts/search_N.short?v=2&kw={query}"
        html = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
        obj = bs(html.read(), features="html.parser")
        tags = obj.find_all("div", "popular__item", limit=3)
        search_result = len(tags)
        for item in tags:
            url = f"https:{item.find('div', 'mask').find('a').attrs['href']}"
            res = item.find('div', 'reccomends-text')
            res1 = res.find('a').get_text()
            res2 = item.find('div', 'author').get_text()
            if not (title.lower() in res1.lower()
                    and author.lower() in res2.lower()):
                continue
            price = item.find('div', 'price').find("span").get_text()
            price = float(price.split()[0])
            return price, url

    if site == 'bookclub.ua':
        query = quote_plus(title, encoding="windows-1251")
        url = f"https://{site}/ukr/search/index.html?search={query}"
        req = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
        html = bs(req.read(), features="html.parser")
        obj = html.find("div", "search-results")
        search_result = obj.find('div', 'main-search').string
        if 'знайдено 0' in search_result:
            return None
        url = f"https://bookclub.ua/{obj.find('a').attrs['href']}"
        html = bs(urlopen(url).read(), "html.parser")
        '''
        url = obj.find('a').attrs['href']
        html = bs(urlopen('https://www.bookclub.ua/' + url).read(), "html.parser")'''
        descriptions = html.findAll('div', 'prd-attr-descr')
        if not (title.lower() in descriptions[1].string.lower() and author.lower() in descriptions[2].string.lower()):
            return None

        price = html.find('div', 'prd-your-price-numb').get_text().split()[0]
        return float(price), url

    if site == 'vsiknygy.com.ua':
        url = f"https://{site}/books/?q={quote(title)}&="
        html = bs(urlopen(url).read(), features="html.parser")
        obj = html.find('div', 'bxr-element-container')
        if not obj:
            return None
        url = f"https://{site}{obj.find('a').attrs['href']}"
        html = bs(urlopen(url).read(), "html.parser")
        res = html.find('h1').string
        if res.lower() != title.lower():
            return None
        res1 = html.find('td', 'bxr-props-data').string
        if res1.split()[0] != author:
            return None
        price = html.find('span', 'bxr-market-current-price bxr-market-format-price')
        price = price.get_text().split()[0]
        return float(price), url

    if site == 'yakaboo.ua':

        query = quote_plus(title)
        url = f"https://{site}/ua/search/?multi=0&cat=&q={query}"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        obj = bs(urlopen(req).read(), features="html.parser")
        tags = obj.find_all("div", "dynamic-info", limit=4)
        for item in tags:
            url = f"https:{item.find('a').attrs['href']}"
            check_1 = item.find('a', 'product-name').get_text()
            check_2 = item.find('div', 'product-author').get_text()
            if not (title.lower() in check_1.lower()
                    and author.lower() in check_2.lower()):
                continue
            if not item.find('div', 'day_delivery'):
                continue
            price = item.find('span', 'price').get_text().split()[0]
            return float(price), url

        query = translit(title)
        url = f"https://{site}/ua/{query}.html"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            obj = bs(urlopen(req).read(), features="html.parser")
        except:
            return None
        check_1 = obj.find('div', 'product-title').find('h1').get_text()
        check_2 = obj.find('table', 'product-attributes__table').find('a').get_text()
        if (title.lower() in check_1.lower() and author.lower() in check_2.lower()
                and 'Паперова книга' in obj.find('div', 'product-sku').get_text()):
            price = obj.find('span', 'price').find('span').get_text()
            return float(price), url

    if site == 'starylev.com.ua':
        query = quote_plus(title)
        url = f"https://{site}/search/node/{query}"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        obj = bs(urlopen(req).read(), features="html.parser")
        cont = obj.find('div', 'container vsl-search-results')
        tags = cont.find_all("a", limit=9)
        for item in tags[::3]:
            url = f"https://{site}{item.attrs['href']}"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            obj = bs(urlopen(req).read(), features="html.parser")
            try:
                cont = obj.find('div', 'col-md-6')
                if 'Паперова' not in cont.find('div', 'switch_book_type').find('a').get_text():
                    continue
            except:
                continue
            cont = obj.find('div', 'col-md-6 vsl-book-info')
            check_1 = cont.find('h1').get_text()
            check_2 = cont.find('div', 'vsl-author').find('a').get_text()
            if not (title.lower() in check_1.lower()
                    and author.lower() in check_2.lower()):
                continue
            cont = obj.find('div', 'col-md-6').find('div', 'vsl-book-btns')
            price = cont.find('span', 'vsl-button vsl-button-price').get_text().split()[0]
            return float(price), url


def get_delivery(site):
    if site == 'bookclub.ua':
        url = f"https://{site}/ukr/help/delivery/"
        html = bs(urlopen(url).read(), features="html.parser")
        obj = html.find('div', 'newscontent').find('ul').find('li').find('strong')
        delivery = float(obj.get_text().split()[0])
        obj = html.find('a', '_head_bl_free_deliv pointer')
        free = float(obj.get_text().split()[-2])
        return delivery, free

    if site == 'vsiknygy.com.ua':
        url = f"https://{site}/about/shipping/"
        html = bs(urlopen(url).read(), features="html.parser")
        obj = html.find('div', 'col-lg-9 col-md-9 col-sm-12 col-xs-12 pull-right')
        delivery = None
        for item in obj.findAll('li'):
            text = item.get_text()
            if text.startswith('Р”Рѕ РІС–РґРґС–Р»РµРЅРЅСЏ'):
                delivery = float(text.split()[-2])
                continue
            if delivery:
                free = float(text.split()[3])
                return delivery, free

    if site == 'bambook.com':
        url = f"https://{site}/about/ua/"
        obj = bs(urlopen(url).read(), features="html.parser")
        text = obj.find_all('ul')[15].get_text().split()
        for item in text:
            try:
                delivery = float(item)
                return delivery, inf
            except:
                continue

    if site == 'yakaboo.ua':
        url = f"https://{site}/ua/delivery/"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        obj = bs(urlopen(req).read(), features="html.parser")
        for item in obj.find_all('p'):
            text = item.get_text()
            exp = 'Вартість доставки фіксована і складає '
            if exp in text:
                index = text.find(exp)
                delivery = float(text[len(exp):text.find(' грн')])
                return delivery, inf

    if site == 'starylev.com.ua':
        url = f"https://{site}/shop/delivery"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        obj = bs(urlopen(req).read(), features="html.parser")
        cont = obj.find_all('div', 'panel-body')[3]
        delivery = cont.find_all("span", {"style": "font-size: medium;"})[4].find('strong').get_text().split()[-2]
        free_delivery = float(delivery)
        return 45, free_delivery


if __name__ == '__main__':
    # print(get_price('Шкляр', 'Характерник', 'yakaboo.ua'))
    # print(get_delivery('yakaboo.ua'))
    print(get_delivery('starylev.com.ua'))
