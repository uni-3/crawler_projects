from typing import Tuple, List
from urllib.parse import urljoin
from lxml.html import SelectElement

from parsel import Selector
from requests import Session

PAGER_SELECTOR = "div.item h3 a::attr(href)"

def crawl_pagination(url: str, session) -> Tuple[List, str]:
    """pagenetion pageの取得"""
    print(f'crawl page: {url}')

    res = session.get(url)
    urls, next_page_url = parse_pagination(res.text)

    urls = [urljoin(url, u) for u in urls]
    if next_page_url:
        next_page_url = urljoin(url, next_page_url)
    print(f'found {len(urls)} urls')

    return urls, next_page_url

def parse_pagination(html) -> Tuple[List, str]:
    """find all links and next page in pagination html"""
    sel = Selector(text=html)
    jobs = sel.css(PAGER_SELECTOR).extract()
    next_page = sel.css('a[area-label=Next]::attr(href)').extract_first()

    return jobs, next_page

    
def crawl_page(url, session) -> dict:
    """next pageを返す"""
    print(f'crawling job: {url}')
    res = session.get(url)

    return {
        'url': url,
        **parse_page(res.text)
    }


def parse_page(html) -> dict:
    """get texts for detail page"""
    sel = Selector(html)

    join = lambda css, sep='': sep.join(sel.css(css).extract()).strip()
    first = lambda css: sel.css(css).extract_first(' ').strip()

    item = {}
    item['title'] = sel.css('h2.title::text').extract_first()
    item['description'] = join('div.box-item-details p ::text')

    return item


def crawl(url):
    with Session() as session:
        next_page = url
        while next_page:
            urls, next_page = crawl_pagination(next_page, session)
            for url in urls:
                yield crawl_page(url, session)