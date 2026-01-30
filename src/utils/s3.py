from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import boto3

from src.config.settings import settings


@dataclass(frozen=True)
class S3Location:
    bucket: str
    key: str


def _client():
    return boto3.client("s3")


def enabled() -> bool:
    return settings.DATA_BACKEND == "s3" and bool(settings.S3_BUCKET)


def to_s3_key(local_path: str) -> str:
    p = Path(local_path)
    return f"{settings.S3_PREFIX}/{p.as_posix()}"


def upload_file(local_path: str, s3_key: Optional[str] = None) -> Optional[S3Location]:
    if not enabled():
        return None
    s3_key = s3_key or to_s3_key(local_path)
    _client().upload_file(local_path, settings.S3_BUCKET, s3_key)
    return S3Location(bucket=settings.S3_BUCKET, key=s3_key)


def download_file(s3_key: str, local_path: str) -> str:
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    _client().download_file(settings.S3_BUCKET, s3_key, local_path)
    return local_path
