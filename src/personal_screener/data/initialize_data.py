import logging
import subprocess

from personal_screener.core.logging_config import setup_logging
from personal_screener.core.quotes.enrich_quotes import \
    calculate_indicators_and_signals
from personal_screener.data.base_data.normalize_yf_quotes import \
    normalize_yf_base_data
from personal_screener.data.base_data.yf_data import get_yf_data
from personal_screener.data.base_data.yf_filters import default_filters
from personal_screener.data.cache_manager import (
    CACHE_DIR,
    save_quotes_to_cache,
)
from personal_screener.data.price_history.price_history_cache import \
    get_price_history_or_cache
from personal_screener.schemas.filters import ScreenerFilters
from personal_screener.schemas.quote import Quote

logger = logging.getLogger(__name__)


def initialize_data(filters: ScreenerFilters = default_filters) -> dict[
    str, Quote]:
    """
    Fetch, normalize, enrich, and cache all data needed for the screener.
    Runs once at app startup (skip if cache is fresh).
    """
    print("Initializing data...")
    # TODO: adjust to more complicated cache behavior, with different cache
    #  files
    # if CACHE_FILE.exists() and is_fresh(CACHE_FILE):
    #     return load_quotes_from_cache()

    # 1. Fetch raw screener results (with filters for universe definition)
    raw_quotes = get_yf_data(filters)

    print("got data")

    # 2. Normalize into Quote dataclasses
    tickers, quotes = normalize_yf_base_data(raw_quotes)
    print("normalized data")
    save_quotes_to_cache(quotes)

    # 3. Enrich with indicators (download price history + cache)
    #    Currently: full-list download of ~2 months daily data
    price_history_df = get_price_history_or_cache(tickers)
    enriched_quotes = calculate_indicators_and_signals(
        price_history_df, quotes,
    )

    save_quotes_to_cache(enriched_quotes)
    print("downloaded price history")

    return quotes


if __name__ == "__main__":
    setup_logging()
    initialize_data()

    subprocess.run(["explorer", str(CACHE_DIR)])
