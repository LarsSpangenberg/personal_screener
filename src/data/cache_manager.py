import json
from dataclasses import asdict
from pathlib import Path

from platformdirs import user_cache_dir

from src.schemas.quote import Quote

CACHE_DIR = Path(user_cache_dir("personal_screener", "Lars Spangenberg"))
CACHE_FILE = CACHE_DIR / "quotes.json"


def save_quotes_to_cache(quotes: dict[str, Quote]):
    CACHE_FILE.parent.mkdir(parents = True, exist_ok = True)
    serializable = {ticker: asdict(quote) for ticker, quote in quotes.items()}
    CACHE_FILE.write_text(json.dumps(serializable, indent = 2))


def load_quotes_from_cache() -> dict[str, Quote]:
    data = json.loads(CACHE_FILE.read_text())
    return {ticker: Quote(**fields) for ticker, fields in data.items()}
