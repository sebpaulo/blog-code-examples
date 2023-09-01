import pytest
from pydantic import HttpUrl
from lxml.etree import Element
from scraper.documents import Item
from scraper import webpages



@pytest.fixture
def webpages_filepath():
    return "data/webpage.json"


@pytest.fixture
def xpath_data_example_1():
    return {
            "title": ".//h1/a",
            "link": ".//h1/a",
            "publication_date": ".//time",
            "description": ".//ul[@class=\"ecl-content-block__primary-meta-container\"]/li"
        }

@pytest.fixture
def webpage_data_example_1(xpath_data_example_1):
    return {
            "url": "https://policy.trade.ec.europa.eu/news_en",
            "name": "Commission_News",
            "items": ".//div[@class=\"ecl-content-item-block\"]//article",
            "item_xpath": xpath_data_example_1,
            "pagination": ".//li[@class=\"ecl-pagination__item ecl-pagination__item--next\"]/a"
        }


@pytest.fixture
def webpage_example_1(webpage_data_example_1):
    return webpages.ServerSideWebPage.from_dict(webpage_data_example_1)


@pytest.fixture
def xpath_data_example_2():
    return {
            "title": ".//h3/a/span",
            "link": ".//h3/a",
            "publication_date": ".//div/span[1]",
            "description": ".//p"
        }

@pytest.fixture
def webpage_data_example_2(xpath_data_example_2):
    return {
            "url": "https://www.europarl.europa.eu/committees/en/inta/home/press-releases",
            "name": "EP_press_releases",
            "items": ".//div[@class='erpl_document ']",
            "item_xpath": xpath_data_example_2,
            "load_more_button": ".//button[contains(.,'Load more')]",
            "load_more_max": 2
        }


@pytest.fixture
def webpage_example_2(webpage_data_example_2):
    return webpages.ClientSideWebPage.from_dict(webpage_data_example_2)


@pytest.fixture
def title_element():
    title_el = Element("h1")
    title_el.text = "Example title"
    return title_el


@pytest.fixture
def date_element():
    date_el = Element("span")
    date_el.text = "20 May 2023"
    return date_el


@pytest.fixture
def link_element():
    link_el = Element("a")
    link_el.attrib["href"] = "https://example.com"
    return link_el


@pytest.fixture
def description_element():
    desc_el = Element("p")
    desc_el.text = "This is an example"
    return desc_el


@pytest.fixture
def example_item(title_element, date_element, link_element, description_element):
    return Item(
        title=title_element,
        publication_date=date_element,
        link=(HttpUrl(url="https://example.com"), link_element),
        description=description_element
    )