from abc import ABC
from dataclasses import dataclass

from ..spidertools import Product


@dataclass(frozen=True, eq=False, slots=True)
class BaseSelector(ABC):
    product: Product



