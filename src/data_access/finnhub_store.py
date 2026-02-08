# from __future__ import annotations

# from typing import Any, Dict, List

# from src.config.settings import get_settings
# from src.data_access.snapshot_manager import SnapshotManager
# from src.tools.fetch_finnhub import get_quote_safe, get_profile_safe

# _settings = get_settings()


# class FinnhubStore:
#     def __init__(self):
#         self.snapshots = SnapshotManager(_settings.finnhub_snapshot_dir)

#     def get_finnhub_bundle(self, tickers: List[str]) -> Dict[str, Any]:
#         snap = self.snapshots.load_latest()
#         if snap and self.snapshots.is_fresh(snap, _settings.FINNHUB_SNAPSHOT_MAX_AGE_SECONDS):
#             return {"served_from": "artifact", "artifact_generated_at": snap.generated_at_utc, "payload": snap.payload}

#         payload = self._fetch_live(tickers)
#         self.snapshots.write_latest(source="live", payload=payload)
#         return {"served_from": "live", "artifact_generated_at": None, "payload": payload}

#     def _fetch_live(self, tickers: List[str]) -> Dict[str, Any]:
#         quotes: List[Dict[str, Any]] = []
#         profiles: List[Dict[str, Any]] = []
#         errors: List[Dict[str, Any]] = []

#         for t in tickers:
#             tkr = (t or "").strip().upper()
#             if not tkr:
#                 continue

#             q = get_quote_safe(tkr)
#             if q.get("ok"):
#                 quotes.append({"ticker": tkr, "quote": q.get("data")})
#             else:
#                 errors.append({"ticker": tkr, "stage": "quote", "reason": q.get("error"), "status": q.get("status")})

#             p = get_profile_safe(tkr)
#             if p.get("ok"):
#                 profiles.append({"ticker": tkr, "profile": p.get("data")})
#             else:
#                 errors.append({"ticker": tkr, "stage": "profile", "reason": p.get("error"), "status": p.get("status")})

#         return {"tickers": tickers, "quotes": quotes, "profiles": profiles, "errors": errors}


from __future__ import annotations

from typing import Any, Dict, List, Callable

from config.settings import settings
from data_access.snapshot_manager import SnapshotManager

LiveFetchFn = Callable[[List[str]], Dict[str, Any]]


class FinnhubStore:
    def __init__(self):
        self.snapshots = SnapshotManager(settings.FINNHUB_SNAPSHOT_DIR)

    def get_finnhub_bundle(self, tickers: List[str], live_fetch_fn: LiveFetchFn) -> Dict[str, Any]:
        snap = self.snapshots.load_latest()
        if snap and self.snapshots.is_fresh(snap, settings.FINNHUB_SNAPSHOT_MAX_AGE_SECONDS):
            return {
                "served_from": "artifact",
                "artifact_generated_at": snap.generated_at_utc,
                "payload": snap.payload,
            }

        payload = live_fetch_fn(tickers)
        self.snapshots.write_latest(source="live", payload=payload)
        return {
            "served_from": "live",
            "artifact_generated_at": None,
            "payload": payload,
        }
