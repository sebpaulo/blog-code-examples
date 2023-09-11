from pydantic.dataclasses import dataclass
from pydantic import field_validator, HttpUrl
from datetime import date
from dateutil.parser import parse, ParserError
from urllib.parse import urljoin, urlparse
from lxml.etree import _Element
from typing import NamedTuple


def get_text_from_sub_elements(element: _Element, sep: str = " ") -> str:
    return sep.join(
        (str(t).strip() for t in element.itertext() if str(t).strip() != "")
    )


class Item(NamedTuple):
    title: _Element
    link: tuple[HttpUrl, _Element]
    publication_date: _Element
    description: _Element


@dataclass(frozen=True)
class Document:
    title: str
    link: HttpUrl
    publication_date: date
    description: str

    @field_validator("title", "description", mode="before")
    def validate_text(cls: "Document", element: _Element) -> str:
        txt = get_text_from_sub_elements(element)
        if len(txt.strip()) == 0:
            raise ValueError
        return txt.strip()

    @field_validator("publication_date", mode="before")
    def validate_date(cls: "Document", date_element: _Element) -> date:
        date_str = get_text_from_sub_elements(date_element)
        if not date_str:
            raise TypeError
        try:
            return parse(date_str).date()
        except ParserError:
            raise ValueError

    @field_validator("link", mode="before")
    def validate_link(cls: "Document", link_info: tuple[HttpUrl, _Element]) -> HttpUrl:
        base_url, link_element = link_info
        link = link_element.get("href")
        if link is None:
            raise TypeError
        parsed_link = urlparse(link)
        if (len(parsed_link.scheme) == 0) or (len(parsed_link.netloc) == 0):
            return HttpUrl(urljoin(str(base_url), link))
        return HttpUrl(link)
