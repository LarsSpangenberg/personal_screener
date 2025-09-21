# src/personal_screener/schemas/default_scoring_template.py

from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.weighted_condition import make_weighted

default_scoring_template = ScoringTemplate(
    # === Base data ===
    avg_vol = make_weighted(1, ("GTE", 1_000_000)),
    market_cap = make_weighted(1, "MID"),
    ma50 = make_weighted(10, ("LTE", "LOW")),
    ma200 = make_weighted(10, ("LTE", "LOW")),

    # === Tiered price ranges ===
    tiered_price_range = [
        make_weighted(3, (20, 50)),
        make_weighted(1, (50, 100)),
    ],

    # === Signals ===
    is_3ma_trending_up = 100,
    is_10ma_trending_up = 100,
)
