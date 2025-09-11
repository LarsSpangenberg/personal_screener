import logging
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from src.data.cache_manager import CACHE_DIR

logger = logging.getLogger(__name__)


def download_full_price_history(
    tickers: list[str],
    months_back: int = 2,
    cache_filename: str = "price_history.parquet",
) -> pd.DataFrame:
    """
    Download daily price history for the given tickers and cache to JSON.

    Args:
        tickers: List of ticker symbols.
        months_back: How many months of history to fetch (default: 2).
        cache_filename: Name of the cache file to write.

    Returns:
        DataFrame with OHLCV data grouped by ticker.
    """
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days = 30 * months_back)

    logger.info(
        "Downloading price history for %d tickers from %s to %s",
        len(tickers),
        start_date,
        end_date,
    )

    df = yf.download(
        tickers = tickers,
        start = start_date,
        end = end_date,
        interval = "1d",
    )

    # Ensure cache directory exists
    cache_dir = CACHE_DIR
    cache_dir.mkdir(parents = True, exist_ok = True)
    cache_path = cache_dir / cache_filename

    # Save as Parquet (preserves MultiIndex columns + datetimes)
    df.to_parquet(cache_path, engine = "pyarrow")

    logger.info("Saved price history to cache: %s", cache_path)

    return df
