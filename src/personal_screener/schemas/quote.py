from dataclasses import dataclass
from typing import Optional


@dataclass
class Quote:
    # base data
    symbol: str
    price: float
    avg_vol: int
    market_cap: int
    ma50: Optional[float] = None
    ma200: Optional[float] = None

    # calculated indicators
    ma3: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    rsi: Optional[float] = None

    # Signals
    is_3ma_trending_up: bool = False
    is_10ma_trending_up: bool = False
