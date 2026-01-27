from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from src.config.settings import settings
from src.utils.helpers import write_json
from src.utils.s3 import upload_file


def _fetch_yfinance_quote(ticker: str) -> Dict[str, Any]:
    try:
        import yfinance as yf
    except Exception as e:
        raise RuntimeError("yfinance not installed. Add yfinance to requirements.txt") from e

    t = yf.Ticker(ticker)
    info = {}
    try:
        info = t.fast_info  # fast_info is lighter
    except Exception:
        pass

    out = {
        "ticker": ticker,
        "last_price": info.get("last_price") if hasattr(info, "get") else None,
        "previous_close": info.get("previous_close") if hasattr(info, "get") else None,
        "market_cap": info.get("market_cap") if hasattr(info, "get") else None,
        "currency": info.get("currency") if hasattr(info, "get") else None,
    }
    return out


def ingest_daily_market_snapshot(run_date: str | None = None) -> str:
    settings.ensure_dirs()

    run_date = run_date or datetime.utcnow().strftime("%Y-%m-%d")
    out_path = Path(settings.MARKET_SNAPSHOT_DIR) / f"market_{run_date}.json"

    rows: List[Dict[str, Any]] = []
    for t in settings.tickers_list():
        rows.append(_fetch_yfinance_quote(t))
        time.sleep(settings.REQUEST_SLEEP_SECONDS)

    write_json(str(out_path), {"run_date": run_date, "rows": rows})
    upload_file(str(out_path))
    return str(out_path)
