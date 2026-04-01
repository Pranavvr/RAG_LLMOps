# from __future__ import annotations

# from config.settings import settings
# from data_access.snapshot_manager import SnapshotManager
# from tools.fetch_news import _fetch_news_live


# def run_news_snapshot(ds: str | None = None) -> None:
#     payload = _fetch_news_live(query="financial markets")

#     sm = SnapshotManager(settings.NEWS_SNAPSHOT_DIR)
#     sm.write_latest(source="scheduled", payload=payload)

#     print("News snapshot refreshed")


from pathlib import Path

from config.settings import settings
from data_access.snapshot_manager import SnapshotManager
from tools.fetch_news import _fetch_news_live
from utils.s3 import enabled, upload_file


def run_news_snapshot(ds: str | None = None) -> None:
    """
    Scheduled news snapshot:
    - For each ticker, fetch Tavily news using a fixed query.
    - Write latest.json under NEWS_SNAPSHOT_DIR.
    - If S3 is configured, upload latest.json so the API can read it later.
    """
    items = []
    for ticker in settings.tickers_list():
        items.extend(_fetch_news_live(f"{ticker} stock news"))

    payload = {"query": "scheduled", "items": items}

    sm = SnapshotManager(Path(settings.NEWS_SNAPSHOT_DIR))
    sm.write_latest(source="scheduled", payload=payload)

    if enabled():
        local_path = Path(settings.NEWS_SNAPSHOT_DIR) / "latest.json"
        upload_file(str(local_path), s3_key=f"{settings.S3_PREFIX}/snapshots/news/latest.json")

    print("News snapshot refreshed")