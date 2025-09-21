from typing import Optional

from personal_screener.schemas.price_value import PriceValue
from personal_screener.schemas.quote import Quote
from personal_screener.schemas.types import PriceOperand


def resolve_operand(quote: Quote, operand: PriceOperand) -> Optional[float]:
    if operand is None:
        return None
    if isinstance(operand, PriceValue):
        return operand.resolve(quote)
    if isinstance(operand, (int, float)):
        return float(operand)
    if operand in ("OPEN", "HIGH", "LOW", "CLOSE"):
        return getattr(quote, operand.lower())
    raise ValueError(f"Unsupported operand type: {operand}")
