from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_utc_iso(dt: str) -> Optional[datetime]:
    try:
        d = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except Exception:
        return None


def seconds_since(dt_iso: str) -> Optional[int]:
    d = _parse_utc_iso(dt_iso)
    if not d:
        return None
    delta = datetime.now(timezone.utc) - d
    return int(delta.total_seconds())


@dataclass
class Snapshot:
    generated_at_utc: str
    source: str
    payload: Any


class SnapshotManager:
    def __init__(self, dir_path: Path, latest_name: str = "latest.json"):
        self.dir_path = Path(dir_path)
        self.latest_path = self.dir_path / latest_name
        self.dir_path.mkdir(parents=True, exist_ok=True)

    def load_latest(self) -> Optional[Snapshot]:
        if not self.latest_path.exists():
            return None
        try:
            data = json.loads(self.latest_path.read_text())
            return Snapshot(
                generated_at_utc=str(data.get("generated_at_utc") or ""),
                source=str(data.get("source") or ""),
                payload=data.get("payload"),
            )
        except Exception:
            return None

    def is_fresh(self, snap: Snapshot, max_age_seconds: int) -> bool:
        if not snap or not snap.generated_at_utc:
            return False
        age = seconds_since(snap.generated_at_utc)
        if age is None:
            return False
        return age <= int(max_age_seconds)

    def write_latest(self, source: str, payload: Any) -> Snapshot:
        snap = Snapshot(generated_at_utc=utc_now_iso(), source=source, payload=payload)
        out = {"generated_at_utc": snap.generated_at_utc, "source": snap.source, "payload": snap.payload}
        self.latest_path.write_text(json.dumps(out, indent=2))
        return snap
