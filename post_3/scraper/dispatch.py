from functools import singledispatch
from dataclasses import asdict
from collections.abc import Iterator
from scraper import webpages
from scraper.documents import Item
from scraper import spider


@singledispatch
def run_spider(webpage: webpages.BaseWebPage) -> Iterator[Item]:
    page = spider.get_page(webpage.url)
    if page is None:
        return
    items = spider.get_items(page, webpage.items)
    yield from spider.parse_items(items, webpage)


@run_spider.register
def _(webpage: webpages.ServerSideWebPage) -> Iterator[Item]:
    page = spider.get_page(webpage.url)
    if page is None:
        return
    items = spider.get_items(page, webpage.items)
    yield from spider.parse_items(items, webpage)
    next_url = spider.get_next_url(page, webpage.url, webpage.pagination)
    if next_url:
        next_page_data = asdict(webpage)
        next_page_data["url"] = next_url
        next_page = webpage.__class__(**next_page_data)
        yield from run_spider(next_page)


@run_spider.register
def _(webpage: webpages.ClientSideWebPage) -> Iterator[Item]:
    with spider.launch_webdriver(options=spider.set_driver_options()) as driver:
        driver = spider.make_driver_request(driver, webpage.url)
        driver = spider.press_load_more_button(driver, webpage)
        page = spider.get_page_from_driver(driver.page_source)
        items = spider.get_items(page, webpage.items)
        yield from spider.parse_items(items, webpage)
