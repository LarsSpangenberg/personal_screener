import pandas as pd

from src.data.cache_manager import CACHE_DIR
from src.data.price_history.download_price_history import \
    download_full_price_history
from src.data.quote_freshness import is_fresh


def load_price_history_from_cache(
    cache_filename: str = "price_history.json",
) -> pd.DataFrame:
    """Read cached price history JSON back into a DataFrame (orient='split')."""
    cache_path = CACHE_DIR / cache_filename
    return pd.read_json(cache_path, orient = "split")


def get_price_history_or_cache(
    tickers: list[str],
    months_back: int = 2,
    cache_filename: str = "price_history.json",
) -> pd.DataFrame:
    """
    Temporary helper: return cached DataFrame if fresh; else download+cache.
    """
    cache_path = CACHE_DIR / cache_filename
    if cache_path.exists() and is_fresh(cache_path):
        return load_price_history_from_cache(cache_filename)

    # Falls back to your existing downloader (which writes the JSON cache)
    return download_full_price_history(
        tickers = tickers,
        months_back = months_back,
        cache_filename = cache_filename,
    )
