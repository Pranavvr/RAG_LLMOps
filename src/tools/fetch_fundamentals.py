from __future__ import annotations

from typing import Any, Dict, Optional
import pandas as pd

from config.settings import settings


_cached_df = None


def _load_df():
    global _cached_df
    if _cached_df is not None:
        return _cached_df
    if settings.FUNDAMENTALS_CLEAN_PARQUET.endswith(".parquet"):
        _cached_df = pd.read_parquet(settings.FUNDAMENTALS_CLEAN_PARQUET)
    else:
        _cached_df = pd.read_csv(settings.FUNDAMENTALS_CSV)
    _cached_df.columns = [c.strip() for c in _cached_df.columns]
    return _cached_df


def fetch_fundamentals_by_symbol(symbol: str) -> Optional[Dict[str, Any]]:
    df = _load_df()
    symbol = symbol.upper().strip()

    for col in ["Symbol", "symbol", "Ticker", "ticker"]:
        if col in df.columns:
            hit = df[df[col].astype(str).str.upper() == symbol]
            if len(hit) > 0:
                return hit.iloc[0].to_dict()

    return None
