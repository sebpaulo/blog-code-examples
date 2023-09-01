from scraper import webpages
from pydantic import HttpUrl
from typing import Type


def test_item_xpath(xpath_data_example_1):
    item_xpath = webpages.ItemXPath(**xpath_data_example_1)
    assert isinstance(item_xpath, webpages.ItemXPath)
    assert isinstance(item_xpath.title, str)


def test_server_webpage(webpage_data_example_1):
    webpage = webpages.ServerSideWebPage.from_dict(webpage_data_example_1)
    assert isinstance(webpage, webpages.ServerSideWebPage)
    assert isinstance(webpage.url, type(HttpUrl))
    assert isinstance(webpage.name, str)


def test_client_webpage(webpage_data_example_2):
    webpage = webpages.ClientSideWebPage.from_dict(webpage_data_example_2)
    assert isinstance(webpage, webpages.ClientSideWebPage)
    assert isinstance(webpage.url, HttpUrl)
    assert isinstance(webpage.name, str)


def test_list_from_json(webpages_filepath):
    webpage_list = webpages.BaseWebPage.list_from_json(webpages_filepath)
    assert isinstance(webpage_list, list)
    assert len(webpage_list) == 2
    assert isinstance(webpage_list[0], webpages.ServerSideWebPage)
    assert isinstance(webpage_list[1], webpages.ClientSideWebPage)


def test_get_webpage_type(webpage_data_example_1, webpage_data_example_2):
    wp_type_1 = webpages.get_webpage_type(webpage_data_example_1)
    wp_type_2 = webpages.get_webpage_type(webpage_data_example_2)
    assert wp_type_1 == webpages.ServerSideWebPage
    assert wp_type_2 == webpages.ClientSideWebPage