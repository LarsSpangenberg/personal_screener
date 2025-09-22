from dataclasses import dataclass
from typing import Optional, Tuple, Union

from personal_screener.schemas.quote import Quote
from personal_screener.schemas.types import Number, OHLC, Operator

# PriceValue Types
PriceOperand = Number | OHLC | "PriceValue"
PriceOperatorCondition = Tuple[Operator, PriceOperand]
PriceBetweenCondition = Tuple[Optional[PriceOperand], Optional[PriceOperand]]


@dataclass
class PriceValue:
    source: Union[Number, OHLC]
    offset: Optional[float] = None
    offset_as_pct: bool = False

    def resolve(self, quote: Quote) -> Optional[float]:
        """
        Resolve the PriceValue against a Quote, applying offsets if needed.
        """
        # Direct numeric
        if isinstance(self.source, (int, float)):
            value = float(self.source)
        else:
            # OHLC mapping
            if self.source == "OPEN":
                value = quote.open
            elif self.source == "HIGH":
                value = quote.high
            elif self.source == "LOW":
                value = quote.low
            elif self.source == "CLOSE":
                value = quote.close
            else:
                raise ValueError(f"Unknown price source: {self.source}")

        if value is None:
            return None

        # Apply offsets
        if self.offset:
            if self.offset_as_pct:
                value *= (1 + self.offset)
            else:
                value += self.offset

        return value
