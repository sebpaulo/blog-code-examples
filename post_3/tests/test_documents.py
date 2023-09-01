from lxml.etree import _Element
from scraper.documents import Item, Document


def test_item(title_element, date_element, link_element, description_element):
    item = Item(
        title=title_element,
        publication_date=date_element,
        link=link_element,
        description=description_element
    )
    assert isinstance(item, Item)
    assert isinstance(item.title, _Element)


def test_document(example_item):
    document = Document(
        title=example_item.title,
        publication_date=example_item.publication_date,
        link=example_item.link,
        description=example_item.description
    )
    assert isinstance(document, Document)
    assert document.title == example_item.title.text


def test_document_from_item_asdict(example_item):
    document = Document(**example_item._asdict())
    assert isinstance(document, Document)