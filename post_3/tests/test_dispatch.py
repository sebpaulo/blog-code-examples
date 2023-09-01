from lxml.etree import _Element
from scraper.dispatch import run_spider
from scraper.documents import Item


def test_run_spider_server_side(webpage_example_1):
    results = []
    for item in run_spider(webpage_example_1):
        results.append(item)
        if len(results) == 15: # only scrape until the second page 
            break
    assert len(results) == 15
    assert isinstance(results[0], Item)
    for k in ["title", "publication_date", "description"]:
        assert isinstance(getattr(results[0], k),  _Element)
    assert isinstance(results[0].link, tuple)
    

def test_run_spider_client_side(webpage_example_2):
    results = []
    for item in run_spider(webpage_example_2):
        results.append(item)
    assert len(results) == 30 # after two load more clicks
    assert isinstance(results[0], Item)
    for k in ["title", "publication_date", "description"]:
        assert isinstance(getattr(results[0], k),  _Element)
    assert isinstance(results[0].link, tuple)