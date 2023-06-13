from ..spidertools import Product
from ._base_selector import BaseSelector

from dataclasses import dataclass


@dataclass(frozen=True, eq=False, slots=True)
class SilpoSelector(BaseSelector):
    partial_url_product_list: str


@dataclass(frozen=True, eq=False, slots=True)
class SilpoXpath(SilpoSelector):
    partial_url_product_list: str = "//a[@class='image-content-wrapper']/@href"
    product_is_over: str = "//div[@class='add-to-comment-btn']"
    product: int = 1