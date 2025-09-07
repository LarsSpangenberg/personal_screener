from dataclasses import dataclass
from typing import Optional


@dataclass
class Quote:
    symbol: str
    price: float
    avg_vol: int
    market_cap: int
    ma50: Optional[float] = None
    ma200: Optional[float] = None
