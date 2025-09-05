import json
import logging
import time
from datetime import datetime
from pathlib import Path

import yfinance as yf
from platformdirs import user_cache_dir
from yfinance import EquityQuery

from src.core.logging_config import setup_logging

logger = logging.getLogger(__name__)

DEFAULT_CACHE_NAME = 'initial_data_cache'
MIN_API_THROTTLE = 0.5

default_query = EquityQuery(
    'AND', [
        EquityQuery('EQ', ['region', 'us']),  # type: ignore
        EquityQuery('GTE', ['avgdailyvol3m', 500000]),  # type: ignore
        EquityQuery('BTWN', ['eodprice', 7, 100]),  # type: ignore
    ],
)


def get_yf_data(
    query = default_query, quote_limit_per_page = 250,
    throttle = MIN_API_THROTTLE, cache_name = DEFAULT_CACHE_NAME,
    force_refresh = False,
) -> list[dict]:
    """
    Fetches data with the yfinance library using the screen method.

    This method accepts a yfinance equity query and returns the total amount of
    quotes found by the screener. Check yfinance API documentation for
    acceptable query parameters under `EquityQuery`. If the result total
    exceeds the max 250 quote limit, multiple requests will be made using
    the throttle, as long as the page_limit is 250 or higher. Since this
    screener is only used for daily data, the result will be cached on the
    local file system and reused after the first use of the day and after
    the first use after 4 PM of the day (Market Close Eastern).

    Result
    -----------
    raw quote data from the yfinance.screen method.
    """
    all_quotes = []
    now = datetime.now()
    date_today = now.strftime("%m%d%Y")
    after_4pm = now.hour >= 16

    base_dir = Path(user_cache_dir())
    cache_dir = _get_cache_dir()
    cache_file_path = (cache_dir / cache_name).with_suffix('.json')

    if not force_refresh and cache_file_path.exists():
        with open(cache_file_path, "r") as f:
            cache = json.load(f)
        cached_date = cache.get('date')
        cached_hour = cache.get('hour', 0)
        if cached_date == date_today and (cached_hour >= 16 or not after_4pm):
            all_quotes = cache.get("quotes")
            logger.info(
                f"Cache hit: loaded {len(all_quotes)} quotes from "
                f"{cache_file_path.relative_to(base_dir)}",
            )

    if len(all_quotes) == 0:
        logger.info("Cache miss: fetching data from API")
        all_quotes = _fetch_data(query, quote_limit_per_page, throttle)
        cache = {
            "date": date_today,
            "hour": now.hour,
            "quotes": all_quotes,
        }
        with open(cache_file_path, 'w') as f:
            json.dump(cache, f)
        logger.info(
            f"Cached {len(all_quotes)} quotes to {cache_file_path.relative_to(base_dir)}",
        )

    return all_quotes


def _fetch_data(query, quote_limit_per_page, throttle) -> list[dict]:
    all_quotes = []
    throttle = max(throttle, MIN_API_THROTTLE)
    quote_limit_per_page = min(quote_limit_per_page, 250)
    page_count = 1
    total = quote_limit_per_page
    offset = 0

    def fetch_page_and_update():
        nonlocal total, offset, all_quotes
        logger.debug(
            f"Fetching page {page_count}: offset={offset}, page_limit={quote_limit_per_page}",
        )
        result = yf.screen(
            query,
            size = quote_limit_per_page,
            offset = offset,
        )
        if not result or "quotes" not in result:
            raise RuntimeError(f"Failed to fetch page at offset {offset}")
        page_quotes = result["quotes"]
        all_quotes.extend(page_quotes)
        total = int(result['total'])
        offset += int(len(page_quotes))
        return page_quotes

    # first run
    fetch_page_and_update()

    # additional pages
    if quote_limit_per_page >= 250:
        if offset < total:
            logger.info(f"Throttling an paginating result for {total} quotes")

        page_count = 2
        while offset < total:
            time.sleep(throttle)
            new_quotes = fetch_page_and_update()
            logger.debug(f"Fetched {len(new_quotes)} of {total} quotes")
            page_count += 1

    logger.info(f"Finished fetching. Total quotes fetched: {len(all_quotes)}")
    return all_quotes


def _get_cache_dir():
    cache_dir = Path(user_cache_dir("personal_screener", "Lars Spangenberg"))
    cache_dir.mkdir(parents = True, exist_ok = True)
    return cache_dir


if __name__ == "__main__":
    setup_logging()
    data = get_yf_data()
    # directory = _get_cache_dir()
    # subprocess.run(f'explorer "{directory}"')
