import json
from pathlib import Path
from typing import Sequence


def dump_tickers_to_json(
    tickers: Sequence[str], filename: str = "tickers.json",
) -> None:
    """
    Save a list of tickers into a JSON file.

    Args:
        tickers: A sequence of ticker symbols (strings).
        filename: The name of the JSON file to save to.
    """
    path = Path(filename)
    data = {"tickers": list(tickers)}

    with path.open("w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 2)

    print(f"Saved {len(tickers)} tickers to {path.resolve()}")
