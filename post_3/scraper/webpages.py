import sys
from typing import TypeVar, Optional, Any, Type
from collections.abc import Mapping
import dataclasses
import inspect
from pydantic.dataclasses import dataclass
from pydantic import HttpUrl
import json
from pathlib import Path


T = TypeVar("T", bound="BaseWebPage")


def get_webpage_type(wp_data: Mapping[str, Any]) -> Optional["BaseWebPage"]:
    data_keys = set(wp_data.keys())
    for _, cls in inspect.getmembers(
        sys.modules[__name__],
        lambda obj: inspect.isclass(obj)
        and (obj.__module__ == sys.modules[__name__].__name__),
    ):
        if dataclasses.is_dataclass(cls):
            wp_fields = {f.name for f in dataclasses.fields(cls)}
            intersection = data_keys.intersection(wp_fields)
            if data_keys == intersection == wp_fields:
                return cls
    return None


@dataclass(frozen=True)
class ItemXPath:
    title: str
    link: str
    publication_date: str
    description: str


@dataclass(frozen=True)
class BaseWebPage:
    url: HttpUrl
    name: str
    items: str
    item_xpath: ItemXPath

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        item_xpath = ItemXPath(**data["item_xpath"])
        data["item_xpath"] = item_xpath
        return cls(**data)

    @staticmethod
    def list_from_json(filename: Path) -> list["BaseWebPage"]:
        with open(filename, "r") as fp:
            webpage_data: list[dict[str, Any]] = json.load(fp)
        webpages: list[BaseWebPage] = []
        for data in webpage_data:
            wp_type = get_webpage_type(data)
            if wp_type:
                webpage = wp_type.from_dict(data)
                webpages.append(webpage)
        return webpages


@dataclass(frozen=True)
class ServerSideWebPage(BaseWebPage):
    pagination: str


@dataclass(frozen=True)
class ClientSideWebPage(BaseWebPage):
    load_more_button: str
    load_more_max: int
