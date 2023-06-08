from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True, eq=False, slots=True)
class Product:
    name: Any
    product_url: Any
    price: Any
    full_price: Any
    product_weight: Any
    unit: Any
    image_url: Any
    brand: Any
    country: Any
    expiration_date: Any
    calories: Any
    protein: Any
    fats: Any
    carbohydrates: Any
    composition: Any


@dataclass(frozen=True, eq=False, slots=True)
class RawProduct(Product):
    marketplace: str
    name: str
    product_url: str
    price: str
    full_price: Optional[str]
    product_weight: Optional[str]
    unit: Optional[str]
    image_url: Optional[str]
    brand: Optional[str]
    country: Optional[str]
    expiration_date: Optional[str]
    calories: Optional[str]
    protein: Optional[str]
    fats: Optional[str]
    carbohydrates: Optional[str]
    composition: Optional[str]


@dataclass(frozen=True, eq=False, slots=True)
class CleanProduct(Product):  # todo not end
    marketplace: str
    ...
