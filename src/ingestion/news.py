from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from config.settings import settings
from utils.helpers import write_json
from utils.s3 import upload_file


def _fetch_tavily_for_ticker(ticker: str) -> List[Dict[str, Any]]:
    try:
        from tavily import TavilyClient
    except Exception as e:
        raise RuntimeError("tavily-python not installed. Add tavily-python to requirements.txt") from e

    if not settings.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY missing")

    client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    q = f"{ticker} stock news"
    resp = client.search(query=q, max_results=settings.NEWS_MAX_RESULTS)
    results = resp.get("results", []) if isinstance(resp, dict) else []
    out = []
    for r in results:
        out.append(
            {
                "ticker": ticker,
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
                "score": r.get("score"),
            }
        )
    return out


def ingest_daily_news_snapshot(run_date: str | None = None) -> str:
    settings.ensure_dirs()

    run_date = run_date or datetime.utcnow().strftime("%Y-%m-%d")
    out_path = Path(settings.NEWS_SNAPSHOT_DIR) / f"news_{run_date}.json"

    all_rows: List[Dict[str, Any]] = []
    for t in settings.tickers_list():
        rows = _fetch_tavily_for_ticker(t)
        all_rows.extend(rows)
        time.sleep(settings.REQUEST_SLEEP_SECONDS)

    write_json(str(out_path), {"run_date": run_date, "rows": all_rows})
    upload_file(str(out_path))
    return str(out_path)
