# from __future__ import annotations

# import pandas as pd

# from src.config.settings import settings
# from src.utils.s3 import upload_file


# def clean_fundamentals_csv() -> str:
#     settings.ensure_dirs()

#     df = pd.read_csv(settings.FUNDAMENTALS_CSV)

#     df.columns = [c.strip() for c in df.columns]

#     out_path = settings.FUNDAMENTALS_CLEAN_PARQUET
#     df.to_parquet(out_path, index=False)

#     upload_file(out_path)
#     return out_path


from __future__ import annotations

import logging
import pandas as pd
from pathlib import Path
from src.config.settings import settings
from src.embeddings.company_cards import build_company_cards
from src.vectorstore.chroma_store import build_chroma_from_company_cards
from src.embeddings.company_cards import write_company_cards_json


# _settings = get_settings()
log = logging.getLogger(__name__)

def clean_fundamentals_csv_to_parquet() -> None:
    """
    Reads FUNDAMENTALS_CSV and writes FUNDAMENTALS_CLEAN_PARQUET.
    This is the missing piece you are asking about.
    """
    df = pd.read_csv(Path(settings.FUNDAMENTALS_CSV))

    # Minimal cleaning. Can extend later
    df.columns = [c.strip() for c in df.columns]
    df = df.drop_duplicates()

    out_path = Path(settings.FUNDAMENTALS_CLEAN_PARQUET)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(out_path, index=False)
    log.info("Wrote parquet: %s (rows=%s, bytes=%s)", out_path, len(df), out_path.stat().st_size)





def build_company_cards_and_index(rebuild: bool = False) -> None:

    clean_fundamentals_csv_to_parquet()

    texts, metadatas = build_company_cards()
    log.info("Built company cards: %s", len(texts))

    json_path = Path(write_company_cards_json(texts, metadatas))
    log.info("Wrote company cards JSON: %s (bytes=%s)", json_path, json_path.stat().st_size)


    # texts, metadatas = build_company_cards()
    
    # out_path = write_company_cards_json(texts, metadatas)

    build_chroma_from_company_cards(
        texts=texts,
        metadatas=metadatas,
        chroma_dir=Path(settings.CHROMA_PERSIST_DIR),
        collection_name="company_cards",
        rebuild=rebuild,
    )
    
    
    chroma_dir = Path(settings.CHROMA_PERSIST_DIR)
    sqlite_path = chroma_dir / "chroma.sqlite3"

    log.info("Chroma persist dir: %s", chroma_dir)

    if sqlite_path.exists():
        log.info("Chroma sqlite exists: %s (bytes=%s)", sqlite_path, sqlite_path.stat().st_size)
    else:
        log.info("Chroma sqlite not found yet (check directory contents).")