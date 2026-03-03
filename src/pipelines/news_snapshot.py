from __future__ import annotations

from config.settings import settings
from data_access.snapshot_manager import SnapshotManager
from tools.fetch_news import _fetch_news_live


def run_news_snapshot(ds: str | None = None) -> None:
    payload = _fetch_news_live()

    sm = SnapshotManager(settings.NEWS_SNAPSHOT_DIR)
    sm.write_latest(source="scheduled", payload=payload)

    print("News snapshot refreshed")
