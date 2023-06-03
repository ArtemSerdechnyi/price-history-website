from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RawProduct:
    marketplace: str
    name: str
    product_url: str
    price: float
    full_price: Optional[float] = None
    image_url: Optional[str] = None
    product_weight = Optional[float] = None
    brand: Optional[str] = None
    country: Optional[str] = None
    expiration_date: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    fats: Optional[float] = None
    carbohydrates: Optional[float] = None
    composition: Optional[str] = None
