from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, eq=False, slots=True)
class RawProduct:
    marketplace: str
    name: str
    product_url: str
    price: str
    full_price: Optional[str] = None
    product_weight: Optional[str] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None
    brand: Optional[str] = None
    country: Optional[str] = None
    expiration_date: Optional[str] = None
    calories: Optional[str] = None
    protein: Optional[str] = None
    fats: Optional[str] = None
    carbohydrates: Optional[str] = None
    composition: Optional[str] = None

