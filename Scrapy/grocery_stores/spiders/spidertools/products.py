from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True, eq=False, slots=True)
class Product:
    name: Any
    product_url: Any
    price: Any
    full_price: Any
    capacity: Any
    image_url: Any


@dataclass(frozen=True, eq=False, slots=True)
class RawProduct(Product):
    marketplace: str
    name: str
    product_url: str
    price: str
    full_price: str
    capacity: str
    image_url: str


@dataclass(frozen=True, eq=False, slots=True)
class CleanProduct(Product):  # todo not end
    marketplace: str
