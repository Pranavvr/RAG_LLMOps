
from __future__ import annotations

from typing import Any

from ingestion.fundamentals import build_company_cards_and_index


def _to_bool(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    return str(x).lower() in {"1", "true", "yes", "y"}


def run_build_chroma_index(rebuild: bool | str = False) -> None:
    build_company_cards_and_index(rebuild=_to_bool(rebuild))
