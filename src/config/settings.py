# from __future__ import annotations

# import os
# from dataclasses import dataclass
# from pathlib import Path
# from dotenv import load_dotenv


# def _to_int(v: str | None, default: int) -> int:
#     try:
#         return int(v) if v is not None else default
#     except Exception:
#         return default


# @dataclass(frozen=True)
# class Settings:
#     OPENAI_API_KEY: str
#     TAVILY_API_KEY: str
#     FINNHUB_API_KEY: str

#     OPENAI_CHAT_MODEL: str
#     OPENAI_EMBED_MODEL: str

#     FUNDAMENTALS_CSV: str
#     FUNDAMENTALS_CLEAN_PARQUET: str
#     COMPANY_CARDS_JSON: str

#     CHROMA_PERSIST_DIR: str
#     SYMBOL_CACHE_PATH: str

#     NEWS_SNAPSHOT_DIR: str
#     MARKET_SNAPSHOT_DIR: str

#     SNAPSHOT_DATE: str

#     DATA_BACKEND: str
#     S3_BUCKET: str
#     S3_PREFIX: str

#     TICKERS: str
#     NEWS_MAX_RESULTS: int
#     REQUEST_SLEEP_SECONDS: int
#     RETRIEVAL_TOP_K: int

#     def ensure_dirs(self) -> None:
#         Path(self.FUNDAMENTALS_CSV).parent.mkdir(parents=True, exist_ok=True)
#         Path(self.FUNDAMENTALS_CLEAN_PARQUET).parent.mkdir(parents=True, exist_ok=True)
#         Path(self.COMPANY_CARDS_JSON).parent.mkdir(parents=True, exist_ok=True)
#         Path(self.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
#         Path(self.SYMBOL_CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)
#         Path(self.NEWS_SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)
#         Path(self.MARKET_SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)

#     def tickers_list(self) -> list[str]:
#         return [t.strip().upper() for t in self.TICKERS.split(",") if t.strip()]


# def load_settings() -> Settings:
#     load_dotenv()

#     return Settings(
#         OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", "").strip(),
#         TAVILY_API_KEY=os.getenv("TAVILY_API_KEY", "").strip(),
#         FINNHUB_API_KEY=os.getenv("FINNHUB_API_KEY", "").strip(),
#         OPENAI_CHAT_MODEL=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini").strip(),
#         OPENAI_EMBED_MODEL=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large").strip(),
#         FUNDAMENTALS_CSV=os.getenv("FUNDAMENTALS_CSV", "data/raw/fundamentals_2024.csv").strip(),
#         FUNDAMENTALS_CLEAN_PARQUET=os.getenv("FUNDAMENTALS_CLEAN_PARQUET", "data/processed/fundamentals_clean.parquet").strip(),
#         COMPANY_CARDS_JSON=os.getenv("COMPANY_CARDS_JSON", "data/company_cards/company_cards_2024.json").strip(),
#         CHROMA_PERSIST_DIR=os.getenv("CHROMA_PERSIST_DIR", "data/indices/chroma").strip(),
#         SYMBOL_CACHE_PATH=os.getenv("SYMBOL_CACHE_PATH", "data/cache/yahoo_symbol_map.json").strip(),
#         NEWS_SNAPSHOT_DIR=os.getenv("NEWS_SNAPSHOT_DIR", "data/snapshots/news").strip(),
#         MARKET_SNAPSHOT_DIR=os.getenv("MARKET_SNAPSHOT_DIR", "data/snapshots/market").strip(),
#         SNAPSHOT_DATE=os.getenv("SNAPSHOT_DATE", "2024-12-31").strip(),
#         DATA_BACKEND=os.getenv("DATA_BACKEND", "local").strip().lower(),
#         S3_BUCKET=os.getenv("S3_BUCKET", "").strip(),
#         S3_PREFIX=os.getenv("S3_PREFIX", "smart-investor-agent").strip(),
#         TICKERS=os.getenv("TICKERS", "AAPL,MSFT,NVDA").strip(),
#         NEWS_MAX_RESULTS=_to_int(os.getenv("NEWS_MAX_RESULTS"), 5),
#         REQUEST_SLEEP_SECONDS=_to_int(os.getenv("REQUEST_SLEEP_SECONDS"), 1),
#         RETRIEVAL_TOP_K=_to_int(os.getenv("RETRIEVAL_TOP_K"), 6),
#     )


# settings = load_settings()


from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


def _to_int(v: str | None, default: int) -> int:
    try:
        return int(v) if v is not None else default
    except Exception:
        return default


def _to_float(v: str | None, default: float) -> float:
    try:
        return float(v) if v is not None else default
    except Exception:
        return default


def _resolve_path(path_str: str, artifact_root: str) -> str:
    p = Path(path_str)

    # Absolute path stays absolute
    if p.is_absolute():
        return str(p)

    # If ARTIFACT_ROOT is set, map "data/..." under that root by stripping "data/"
    if artifact_root.strip():
        ar = Path(artifact_root).expanduser()
        s = path_str.replace("\\", "/")
        if s.startswith("data/"):
            s = s[len("data/") :]
        return str((ar / s).resolve())

    # Local dev fallback: keep it relative to repo working dir
    return str(p)


@dataclass(frozen=True)
class Settings:
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    FINNHUB_API_KEY: str

    OPENAI_CHAT_MODEL: str
    OPENAI_EMBED_MODEL: str

    # Optional. Set only in AWS:
    # ARTIFACT_ROOT=/mnt/efs/smart-investor-agent
    ARTIFACT_ROOT: str

    FUNDAMENTALS_CSV: str
    FUNDAMENTALS_CLEAN_PARQUET: str
    COMPANY_CARDS_JSON: str

    CHROMA_PERSIST_DIR: str
    SYMBOL_CACHE_PATH: str

    NEWS_SNAPSHOT_DIR: str
    MARKET_SNAPSHOT_DIR: str
    FINNHUB_SNAPSHOT_DIR: str

    SNAPSHOT_DATE: str

    DATA_BACKEND: str
    S3_BUCKET: str
    S3_PREFIX: str

    TICKERS: str
    NEWS_MAX_RESULTS: int
    REQUEST_SLEEP_SECONDS: float
    RETRIEVAL_TOP_K: int

    # Freshness
    MARKET_SNAPSHOT_MAX_AGE_SECONDS: int
    NEWS_SNAPSHOT_MAX_AGE_SECONDS: int
    FINNHUB_SNAPSHOT_MAX_AGE_SECONDS: int

    def ensure_dirs(self) -> None:
        Path(self.FUNDAMENTALS_CSV).parent.mkdir(parents=True, exist_ok=True)
        Path(self.FUNDAMENTALS_CLEAN_PARQUET).parent.mkdir(parents=True, exist_ok=True)
        Path(self.COMPANY_CARDS_JSON).parent.mkdir(parents=True, exist_ok=True)

        Path(self.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.SYMBOL_CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)

        Path(self.NEWS_SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.MARKET_SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.FINNHUB_SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)

    def tickers_list(self) -> list[str]:
        return [t.strip().upper() for t in self.TICKERS.split(",") if t.strip()]


def load_settings() -> Settings:
    load_dotenv()

    artifact_root = os.getenv("ARTIFACT_ROOT", "").strip()

    fundamentals_csv = os.getenv("FUNDAMENTALS_CSV", "data/raw/fundamentals_2024.csv").strip()
    fundamentals_clean = os.getenv("FUNDAMENTALS_CLEAN_PARQUET", "data/processed/fundamentals_clean.parquet").strip()
    company_cards = os.getenv("COMPANY_CARDS_JSON", "data/company_cards/company_cards_2024.json").strip()

    chroma_dir = os.getenv("CHROMA_PERSIST_DIR", "data/indices/chroma").strip()
    symbol_cache = os.getenv("SYMBOL_CACHE_PATH", "data/cache/yahoo_symbol_map.json").strip()

    news_dir = os.getenv("NEWS_SNAPSHOT_DIR", "data/snapshots/news").strip()
    market_dir = os.getenv("MARKET_SNAPSHOT_DIR", "data/snapshots/market").strip()
    finnhub_dir = os.getenv("FINNHUB_SNAPSHOT_DIR", "data/snapshots/finnhub").strip()

    settings = Settings(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", "").strip(),
        TAVILY_API_KEY=os.getenv("TAVILY_API_KEY", "").strip(),
        FINNHUB_API_KEY=os.getenv("FINNHUB_API_KEY", "").strip(),
        OPENAI_CHAT_MODEL=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini").strip(),
        OPENAI_EMBED_MODEL=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large").strip(),
        ARTIFACT_ROOT=artifact_root,
        FUNDAMENTALS_CSV=_resolve_path(fundamentals_csv, artifact_root),
        FUNDAMENTALS_CLEAN_PARQUET=_resolve_path(fundamentals_clean, artifact_root),
        COMPANY_CARDS_JSON=_resolve_path(company_cards, artifact_root),
        CHROMA_PERSIST_DIR=_resolve_path(chroma_dir, artifact_root),
        SYMBOL_CACHE_PATH=_resolve_path(symbol_cache, artifact_root),
        NEWS_SNAPSHOT_DIR=_resolve_path(news_dir, artifact_root),
        MARKET_SNAPSHOT_DIR=_resolve_path(market_dir, artifact_root),
        FINNHUB_SNAPSHOT_DIR=_resolve_path(finnhub_dir, artifact_root),
        SNAPSHOT_DATE=os.getenv("SNAPSHOT_DATE", "2024").strip(),
        DATA_BACKEND=os.getenv("DATA_BACKEND", "local").strip().lower(),
        S3_BUCKET=os.getenv("S3_BUCKET", "").strip(),
        S3_PREFIX=os.getenv("S3_PREFIX", "smart-investor-agent").strip(),
        TICKERS=os.getenv("TICKERS", "AAPL,MSFT,NVDA").strip(),
        NEWS_MAX_RESULTS=_to_int(os.getenv("NEWS_MAX_RESULTS"), 5),
        REQUEST_SLEEP_SECONDS=_to_float(os.getenv("REQUEST_SLEEP_SECONDS"), 1.0),
        RETRIEVAL_TOP_K=_to_int(os.getenv("RETRIEVAL_TOP_K"), 6),
        MARKET_SNAPSHOT_MAX_AGE_SECONDS=_to_int(os.getenv("MARKET_SNAPSHOT_MAX_AGE_SECONDS"), 900),
        NEWS_SNAPSHOT_MAX_AGE_SECONDS=_to_int(os.getenv("NEWS_SNAPSHOT_MAX_AGE_SECONDS"), 21600),
        FINNHUB_SNAPSHOT_MAX_AGE_SECONDS=_to_int(os.getenv("FINNHUB_SNAPSHOT_MAX_AGE_SECONDS"), 3600),
    )

    settings.ensure_dirs()
    return settings


settings = load_settings()
