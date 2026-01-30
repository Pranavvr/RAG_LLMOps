# from __future__ import annotations

# import json
# from pathlib import Path
# from typing import Any, Dict


# def read_json(path: str) -> Any:
#     return json.loads(Path(path).read_text(encoding="utf-8"))


# def write_json(path: str, obj: Any) -> str:
#     p = Path(path)
#     p.parent.mkdir(parents=True, exist_ok=True)
#     p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
#     return str(p)


# def safe_str(v: Any) -> str:
#     if v is None:
#         return ""
#     return str(v)


from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")

    if len(text) > max_len:
        h = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        text = text[: max_len - 11] + "-" + h

    return text or "q"


def safe_json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def safe_json_load(path: Path) -> Optional[Any]:
    
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def http_get_json(
    url: str,
    params: Dict[str, Any],
    timeout: float = 15.0,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    r = requests.get(url, params=params, timeout=timeout, headers=headers)
    return {"status": r.status_code, "ok": r.ok, "text": r.text, "json": (r.json() if r.ok else None)}


def sleep_seconds(seconds: float) -> None:
    if seconds and seconds > 0:
        time.sleep(seconds)
