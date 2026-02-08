# from __future__ import annotations

# import time
# from pathlib import Path
# from typing import Any, Dict, List, Optional

# from src.config.settings import settings
# from src.utils.helpers import read_json
# from src.ingestion.news import _fetch_tavily_for_ticker


# def _latest_snapshot_path() -> Optional[str]:
#     p = Path(settings.NEWS_SNAPSHOT_DIR)
#     files = sorted(p.glob("news_*.json"))
#     if not files:
#         return None
#     return str(files[-1])

# def _is_fresh(path: str, max_age_seconds: int) -> bool:
#     try:
#         mtime = Path(path).stat().st_mtime()
#     except OSError:
#         return False
    
#     age = time.time() -mtime

#     return age <= max_age_seconds

# def fetch_news(ticker: str, allow_live_fallback: bool = True) -> List[Dict[str, Any]]:

#     ticker = ticker.upper().strip()
#     snap = _latest_snapshot_path()

#     max_age = getattr(settings, "NEWS_SNAPSHOT_MAX_AGE_SECONDS", 6 * 60 * 60)

#     if snap and _is_fresh(snap, max_age):
#         data = read_json(snap) or {}
#         rows = data.get("rows") or []
#         return [r for r in rows if (r.get("ticker") or "").upper() == ticker]

#     if allow_live_fallback:
#         return _fetch_tavily_for_ticker(ticker)

#     return []

from __future__ import annotations

from typing import Dict, Any, List, Optional

from tavily import TavilyClient

from config.settings import settings
from data_access.news_store import NewsStore

# _settings = settings()
_tavily: Optional[TavilyClient] = None
_news_store = NewsStore()


def get_tavily() -> TavilyClient:
    global _tavily
    if _tavily is None:
        _tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)
    return _tavily

def _fetch_news_live(query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
    max_results = max_results or settings.NEWS_MAX_RESULTS
    tavily = get_tavily()
    res = tavily.search(query=query, max_results=max_results, include_raw_content=False)

    items: List[Dict[str, Any]] = []
    for r in res.get("results", []) or []:
        items.append({"title": r.get("title"), "url": r.get("url"), "content": r.get("content")})

    return items



def fetch_news(query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
    max_results = max_results or settings.NEWS_MAX_RESULTS

    return _news_store.get_news_bundle(
        query=query,
        max_results=max_results,
        live_fetch_fn=_fetch_news_live,
    )

# def search_news(query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
#     max_results = max_results or settings.NEWS_MAX_RESULTS
#     tavily = get_tavily()
#     res = tavily.search(query=query, max_results=max_results, include_raw_content=False)

#     items: List[Dict[str, Any]] = []
#     for r in res.get("results", []) or []:
#         items.append({"title": r.get("title"), "url": r.get("url"), "content": r.get("content")})
    
#     return items
