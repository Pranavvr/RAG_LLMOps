# from __future__ import annotations

# import time
# from pathlib import Path
# from typing import Any, Dict, Optional

# from src.config.settings import settings
# from src.utils.helpers import read_json
# from src.ingestion.market_data import _fetch_yfinance_quote


# def _latest_snapshot_path() -> Optional[str]:
#     p = Path(settings.MARKET_SNAPSHOT_DIR)
#     files = sorted(p.glob("market_*.json"))
#     if not files:
#         return None
#     return str(files[-1])

# def _is_fresh(path: str, max_age_seconds: int) -> bool:
#     try:
#         mtime = Path(path).stat().st_mtime
#     except OSError:
#         return False
#     age = time.time() - mtime
#     return age <= max_age_seconds


# def fetch_prices(ticker: str, allow_live_fallback: bool = True) -> Dict[str, Any]:
#     ticker = ticker.upper().strip()
#     snap = _latest_snapshot_path()

#     max_age = getattr(settings, "MARKET_SNAPSHOT_MAX_AGE_SECONDS", 15 * 60)


#     if snap and _is_fresh(snap, max_age):
#         data = read_json(snap) or {}
#         rows = data.get("rows") or []
        
#         for r in rows:
#             if (r.get("ticker") or "").upper() == ticker:
#                 return r

#     if allow_live_fallback:
#         return _fetch_yfinance_quote(ticker)

#     return {"ticker": ticker}



from __future__ import annotations

from typing import Optional

import yfinance as yf

from utils.cache import get_cached_symbol, set_cached_symbol


def is_probably_valid_symbol(sym: Optional[str]) -> bool:
    if not sym:
        return False
    s = sym.strip().upper()
    if len(s) < 1 or len(s) > 10:
        return False
    import re
    return bool(re.match(r"^[A-Z0-9\.-]+$", s))


def _yfinance_last_close(yahoo_symbol: str, period: str = "5d") -> Optional[float]:
    try:
        hist = yf.Ticker(yahoo_symbol).history(period=period)
        if hist is None or hist.empty:
            return None
        return float(hist["Close"].iloc[-1])
    except Exception:
        return None


def resolve_yahoo_symbol(symbol: str) -> str:
    s = (symbol or "").strip().upper()
    if not s:
        return s
    cached = get_cached_symbol(s)
    if cached:
        return cached

    candidates = [s]
    if "." in s:
        candidates.append(s.replace(".", "-"))

    for cand in candidates:
        last = _yfinance_last_close(cand, period="5d")
        if last is not None:
            set_cached_symbol(s, cand)
            return cand

    set_cached_symbol(s, s)
    return s


def get_recent_close_safe(symbol: str, period: str = "5d") -> Optional[float]:
    if not is_probably_valid_symbol(symbol):
        return None
    yahoo_sym = resolve_yahoo_symbol(symbol)
    return _yfinance_last_close(yahoo_sym, period=period)
