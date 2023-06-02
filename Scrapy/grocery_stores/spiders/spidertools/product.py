from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    marketplace: str
    name: Optional[str]
    product_url: str
    image_url: str
    price: Optional[str]
    full_price: Optional[str]
    brand: Optional[str]
    country: Optional[str]
    expiration_date: Optional[str]
    calories: Optional[str]
    protein: Optional[str]
    fats: Optional[str]
    carbohydrates: Optional[str]
    composition: Optional[str]
