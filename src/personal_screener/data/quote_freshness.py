from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo  # built-in in Python 3.9+

MARKET_TZ = ZoneInfo("America/New_York")
MARKET_CLOSE = time(16, 0)
REFRESH_DELAY = timedelta(minutes = 5)


def is_fresh(path: Path) -> bool:
    """Check if cache is valid based on Eastern Time market close."""
    if not path.exists():
        return False

    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz = MARKET_TZ)
    now = datetime.now(MARKET_TZ)

    market_close_today = datetime.combine(
        now.date(), MARKET_CLOSE, tzinfo = MARKET_TZ,
    ) + REFRESH_DELAY
    market_close_yesterday = market_close_today - timedelta(days = 1)

    if mtime.date() == now.date():
        return mtime >= market_close_today  # only fresh if updated after today’s close

    if (
            market_close_yesterday <= mtime < market_close_today
            and now < market_close_today
    ):
        # Still fresh window: yesterday's close to today's close
        return True

    return False
