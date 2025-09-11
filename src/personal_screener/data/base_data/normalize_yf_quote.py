import logging
from datetime import datetime

from personal_screener.schemas.quote import Quote

logger = logging.getLogger(__name__)


# === Already used in default query (yf_data.py) ===
# region
# avgdailyvol3m
# eodprice

# === Present in the screener quote ===
# regularMarketPrice
# regularMarketDayLow
# regularMarketDayHigh
# fiftyTwoWeekLow
# fiftyTwoWeekHigh
# fiftyTwoWeekRange
# marketCap
# epsTrailingTwelveMonths
# epsForward
# epsCurrentYear
# earningsTimestamp
# earningsTimestampStart
# earningsTimestampEnd
# dividendYield
# dividendRate
# dividendDate
# averageDailyVolume3Month
# averageDailyVolume10Day
# regularMarketVolume
# regularMarketChangePercent
# fiftyTwoWeekChangePercent
# trailingPE
# forwardPE
# priceToBook
# bookValue
# sharesOutstanding
# regularMarketPreviousClose
# fiftyDayAverage
# twoHundredDayAverage
# analystRating

# === Missing (need other endpoint or calculation) ===
# MA_3
# MA_10
# MA_21
# RSI
# sector
# industry
# sales / revenue
# shortFloat
# newsSentiment
# volatility_weekly
# volatility_monthly

# === Additional useful fields (optional) ===
# nameChangeDate
# prevName
# tradeable
# triggerable
# fullExchangeName
# financialCurrency


def normalize_yf_quote(quote: dict) -> Quote:
    """
    Convert raw quote dict into a normalized schema.
    """
    day_close = quote.get("regularMarketPreviousClose")
    if datetime.now().hour >= 16:
        day_close = quote.get("regularMarketPrice")

    return Quote(
        symbol = quote.get("symbol"),
        price = day_close,
        market_cap = quote.get("marketCap"),
        avg_vol = quote.get("averageDailyVolume3Month"),
        ma50 = quote.get("fiftyDayAverage"),
        ma200 = quote.get("twoHundredDayAverage"), )
