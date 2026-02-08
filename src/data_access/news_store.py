from __future__ import annotations

from typing import Any, Dict, Callable, List, Optional

from config.settings import settings
from data_access.snapshot_manager import SnapshotManager
# from src.tools.fetch_news import search_news

# _settings = get_settings()

LiveFetchFn = Callable[[str, Optional[int]], List[Dict[str, Any]]]


class NewsStore:
    def __init__(self):
        self.snapshots = SnapshotManager(settings.NEWS_SNAPSHOT_DIR)

    def get_news_bundle(self, query: str, max_results: int,
        live_fetch_fn: LiveFetchFn) -> Dict[str, Any]:

        snap = self.snapshots.load_latest()
        if snap and self.snapshots.is_fresh(snap, settings.NEWS_SNAPSHOT_MAX_AGE_SECONDS):
            return {
                "served_from": "artifact",
                "artifact_generated_at": snap.generated_at_utc,
                "payload": snap.payload,
            }

        items = live_fetch_fn(query, max_results)
        payload = {"query": query, "items": items}
        self.snapshots.write_latest(source="live", payload=payload)

        return {
            "served_from": "live",
            "artifact_generated_at": None,
            "payload": payload,
        }
    
        # snap = self.snapshots.load_latest()
        # if snap and self.snapshots.is_fresh(snap, settings.NEWS_SNAPSHOT_MAX_AGE_SECONDS):
        #     return {"served_from": "artifact", "artifact_generated_at": snap.generated_at_utc, "payload": snap.payload}

        # items = search_news(query=query, max_results=settings.NEWS_MAX_RESULTS)
        # payload = {"query": query, "items": items}
        # self.snapshots.write_latest(source="live", payload=payload)
        # return {"served_from": "live", "artifact_generated_at": None, "payload": payload}
