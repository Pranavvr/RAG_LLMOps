from __future__ import annotations

import os
from pathlib import Path
from config.settings import settings
from data_access.snapshot_manager import SnapshotManager
from tools.fetch_market_bundle import _fetch_market_live


def run_market_snapshot(ds: str | None = None) -> None:
    tickers_env = os.getenv("TICKERS")

    if not tickers_env:
        raise ValueError("TICKERS env variable not set")

    tickers = [t.strip() for t in tickers_env.split(",") if t.strip()]

    payload = _fetch_market_live(tickers)

    sm = SnapshotManager(Path(settings.MARKET_SNAPSHOT_DIR))
    sm.write_latest(source="scheduled", payload=payload)

    print("Market snapshot refreshed")
