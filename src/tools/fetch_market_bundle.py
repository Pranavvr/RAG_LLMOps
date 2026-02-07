from __future__ import annotations

from typing import Dict, Any, List

from data_access.market_store import MarketStore
from tools.fetch_prices import get_recent_close_safe
from tools.fetch_finnhub import get_quote_safe, get_profile_safe

_store = MarketStore()


def _fetch_market_live(tickers: List[str]) -> Dict[str, Any]:
    quotes = []
    profiles = []
    errors = []

    clean = [(t or "").strip().upper() for t in tickers if (t or "").strip()]

    for tkr in clean:
        last_close = get_recent_close_safe(tkr)
        if last_close is not None:
            quotes.append({"ticker": tkr, "yfinance_last_close": last_close})

        q = get_quote_safe(tkr)
        if q.get("ok"):
            quotes.append({"ticker": tkr, "finnhub_quote": q["data"]})
        else:
            errors.append({"ticker": tkr, "stage": "quote", "error": q.get("error")})

        p = get_profile_safe(tkr)
        if p.get("ok"):
            profiles.append({"ticker": tkr, "profile": p["data"]})
        else:
            errors.append({"ticker": tkr, "stage": "profile", "error": p.get("error")})

    return {
        "tickers": clean,
        "quotes": quotes,
        "profiles": profiles,
        "errors": errors,
    }


def fetch_market_bundle(tickers: List[str]) -> Dict[str, Any]:
    return _store.get_market_bundle(
        tickers=tickers,
        live_fetch_fn=_fetch_market_live,
    )
