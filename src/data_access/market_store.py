# from __future__ import annotations

# from typing import Any, Dict, List

# from src.config.settings import get_settings
# from src.data_access.snapshot_manager import SnapshotManager
# from src.tools.fetch_prices import get_recent_close_safe
# from src.tools.fetch_finnhub import get_quote_safe, get_profile_safe

# _settings = get_settings()


# class MarketStore:
#     def __init__(self):
#         self.snapshots = SnapshotManager(_settings.market_snapshot_dir)

#     def get_market_bundle(self, tickers: List[str]) -> Dict[str, Any]:
#         snap = self.snapshots.load_latest()
#         if snap and self.snapshots.is_fresh(snap, _settings.MARKET_SNAPSHOT_MAX_AGE_SECONDS):
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

#             last_close = get_recent_close_safe(tkr)
#             if last_close is not None:
#                 quotes.append({"ticker": tkr, "yfinance_last_close": last_close})

#             q = get_quote_safe(tkr)
#             if q.get("ok"):
#                 quotes.append({"ticker": tkr, "finnhub_quote": q.get("data")})
#             else:
#                 errors.append({"ticker": tkr, "stage": "finnhub_quote", "reason": q.get("error"), "status": q.get("status")})

#             p = get_profile_safe(tkr)
#             if p.get("ok"):
#                 profiles.append({"ticker": tkr, "profile": p.get("data")})
#             else:
#                 errors.append({"ticker": tkr, "stage": "finnhub_profile", "reason": p.get("error"), "status": p.get("status")})

#         return {"tickers": tickers, "quotes": quotes, "profiles": profiles, "errors": errors}


from __future__ import annotations

from typing import Any, Dict, List, Callable

from src.config.settings import settings
from src.data_access.snapshot_manager import SnapshotManager

LiveFetchFn = Callable[[List[str]], Dict[str, Any]]


class MarketStore:
    def __init__(self):
        self.snapshots = SnapshotManager(settings.MARKET_SNAPSHOT_DIR)

    def get_market_bundle(
        self,
        tickers: List[str],
        live_fetch_fn: LiveFetchFn,
    ) -> Dict[str, Any]:
        snap = self.snapshots.load_latest()
        if snap and self.snapshots.is_fresh(
            snap, settings.MARKET_SNAPSHOT_MAX_AGE_SECONDS
        ):
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
