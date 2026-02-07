from __future__ import annotations

from typing import List, Any, Dict

from config.settings import settings
from utils.helpers import http_get_json, sleep_seconds

from data_access.finnhub_store import FinnhubStore

_store = FinnhubStore()

# _settings = get_settings()
FINNHUB_BASE = "https://finnhub.io/api/v1"


def finnhub_get_safe(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{FINNHUB_BASE}/{path.lstrip('/')}"
    p = dict(params)
    p["token"] = settings.FINNHUB_API_KEY
    try:
        out = http_get_json(url, p, timeout=15.0)
        sleep_seconds(float(settings.REQUEST_SLEEP_SECONDS))
        if not out["ok"]:
            return {"ok": False, "status": out["status"], "data": {}, "error": out["text"][:200]}
        return {"ok": True, "status": out["status"], "data": out["json"] or {}, "error": None}
    except Exception as e:
        return {"ok": False, "status": None, "data": {}, "error": str(e)}


def get_quote_safe(symbol: str) -> Dict[str, Any]:
    if not symbol:
        return {"ok": False, "status": None, "data": {}, "error": "missing_symbol"}
    return finnhub_get_safe("quote", {"symbol": symbol})


def get_profile_safe(symbol: str) -> Dict[str, Any]:
    if not symbol:
        return {"ok": False, "status": None, "data": {}, "error": "missing_symbol"}
    return finnhub_get_safe("stock/profile2", {"symbol": symbol})




def _fetch_finnhub_live(tickers: List[str]) -> Dict[str, Any]:
    quotes: List[Dict[str, Any]] = []
    profiles: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    for t in tickers:
        tkr = (t or "").strip().upper()
        if not tkr:
            continue

        q = get_quote_safe(tkr)
        if q.get("ok"):
            quotes.append({"ticker": tkr, "quote": q.get("data")})
        else:
            errors.append({"ticker": tkr, "stage": "quote", "reason": q.get("error"), "status": q.get("status")})

        p = get_profile_safe(tkr)
        if p.get("ok"):
            profiles.append({"ticker": tkr, "profile": p.get("data")})
        else:
            errors.append({"ticker": tkr, "stage": "profile", "reason": p.get("error"), "status": p.get("status")})

    return {"tickers": tickers, "quotes": quotes, "profiles": profiles, "errors": errors}


def get_finnhub_bundle(tickers: List[str]) -> Dict[str, Any]:
    return _store.get_finnhub_bundle(tickers=tickers, live_fetch_fn=_fetch_finnhub_live)
