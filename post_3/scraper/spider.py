import requests
from lxml import html
from lxml.etree import _Element
from time import sleep
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Optional
from collections.abc import Mapping, Iterator, Sequence, Generator
from pydantic import HttpUrl
from urllib.parse import urljoin, urlparse
from scraper.documents import Item
from scraper import webpages


headers: Mapping[str, str] = {}


def make_request(url: HttpUrl, headers: Mapping[str, str]) -> requests.Response:
    return requests.get(str(url), headers=headers, timeout=30)


def set_driver_options() -> webdriver.FirefoxOptions:
    options = webdriver.FirefoxOptions()
    # add options if needed like on the following line
    # options.add_argument(f'--user-agent="{user_agent}"')
    return options


@contextmanager
def launch_webdriver(
    options: webdriver.FirefoxOptions,
) -> Generator[WebDriver, None, None]:
    with webdriver.Firefox(options=options) as driver:
        yield driver


def make_driver_request(driver: WebDriver, url: HttpUrl) -> WebDriver:
    driver.get(str(url))
    return driver


def get_page_from_driver(page_source: str) -> _Element:
    return html.fromstring(page_source)


def get_page(url: HttpUrl, max_retries: int = 3) -> _Element:
    for _ in range(max_retries):
        try:
            response = make_request(url, headers)
        except requests.exceptions.ConnectionError:
            sleep(5)
            continue
        else:
            return html.fromstring(response.text)
    raise Exception(f"Page not found ({url}).")


def press_load_more_button(
    driver: WebDriver, wp: webpages.ClientSideWebPage
) -> WebDriver:
    for _ in range(wp.load_more_max):
        try:
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, wp.load_more_button))
            )
            driver.execute_script("arguments[0].click();", button)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, wp.load_more_button))
            )
        except TimeoutException:
            break
    return driver


def get_items(html: _Element, items_xpath: str) -> list[_Element]:
    items = html.findall(items_xpath)
    return items


def create_lxml_element(item: _Element, xpath: str) -> _Element:
    el = item.find(xpath)
    if el is None:
        raise TypeError
    return el


def populate_item(item: _Element, wp: webpages.BaseWebPage) -> Item:
    return Item(
        title=create_lxml_element(item, wp.item_xpath.title),
        publication_date=create_lxml_element(item, wp.item_xpath.publication_date),
        link=(wp.url, create_lxml_element(item, wp.item_xpath.link)),
        description=create_lxml_element(item, wp.item_xpath.description),
    )


def parse_items(items: Sequence[_Element], wp: webpages.BaseWebPage) -> Iterator[Item]:
    for item in items:
        try:
            yield populate_item(item, wp)
        except TypeError:
            continue


def get_next_url(
    page: _Element, page_url: HttpUrl, pagination_xpath: str
) -> Optional[HttpUrl]:
    next_page = page.find(pagination_xpath)
    if next_page is None:
        return None
    next_url = next_page.get("href")
    if next_url is None:
        return None
    parsed_url = urlparse(next_url)
    if not parsed_url.scheme:
        return HttpUrl(urljoin(str(page_url), next_url))
    return HttpUrl(next_url)
