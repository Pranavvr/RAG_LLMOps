# from __future__ import annotations

# from pathlib import Path
# from typing import Any, Dict, Optional

# from src.utils.helpers import read_json, write_json


# def load_cache(path: str) -> Dict[str, Any]:
#     p = Path(path)
#     if not p.exists():
#         return {}
#     try:
#         data = read_json(str(p))
#         return data if isinstance(data, dict) else {}
#     except Exception:
#         return {}


# def save_cache(path: str, data: Dict[str, Any]) -> str:
#     return write_json(path, data)


# def get_cached(cache: Dict[str, Any], key: str) -> Optional[Any]:
#     return cache.get(key)


# from __future__ import annotations

# import json
# from pathlib import Path
# from typing import Dict, Optional

# from src.config.settings import settings

# # settings = get_settings()
# _CACHE_PATH: Path = settings.SYMBOL_CACHE_PATH

# _YAHOO_SYMBOL_CACHE: Dict[str, str] = {}


# def load_symbol_cache() -> Dict[str, str]:
#     global _YAHOO_SYMBOL_CACHE
#     if _CACHE_PATH.exists():
#         try:
#             _YAHOO_SYMBOL_CACHE = json.loads(_CACHE_PATH.read_text())
#         except Exception:
#             _YAHOO_SYMBOL_CACHE = {}
#     else:
#         _YAHOO_SYMBOL_CACHE = {}
#     return _YAHOO_SYMBOL_CACHE


# def save_symbol_cache() -> None:
#     _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
#     _CACHE_PATH.write_text(json.dumps(_YAHOO_SYMBOL_CACHE, indent=2))


# def get_cached_symbol(key: str) -> Optional[str]:
#     if not _YAHOO_SYMBOL_CACHE:
#         load_symbol_cache()
#     return _YAHOO_SYMBOL_CACHE.get(key)


# def set_cached_symbol(key: str, value: str) -> None:
#     if not _YAHOO_SYMBOL_CACHE:
#         load_symbol_cache()
#     _YAHOO_SYMBOL_CACHE[key] = value
#     save_symbol_cache()






from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

from src.config.settings import settings

_CACHE_PATH = Path(settings.SYMBOL_CACHE_PATH)
_symbol_map: Dict[str, str] = {}
_loaded = False


def load_symbol_cache() -> None:
    global _loaded, _symbol_map
    if _loaded:
        return
    if _CACHE_PATH.exists():
        try:
            _symbol_map = json.loads(_CACHE_PATH.read_text())
        except Exception:
            _symbol_map = {}
    _loaded = True


def get_cached_symbol(sym: str) -> Optional[str]:
    load_symbol_cache()
    return _symbol_map.get(sym)


def set_cached_symbol(original: str, resolved: str) -> None:
    load_symbol_cache()
    _symbol_map[original] = resolved
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CACHE_PATH.write_text(json.dumps(_symbol_map, indent=2))
