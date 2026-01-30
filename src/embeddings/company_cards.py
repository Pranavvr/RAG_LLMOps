# from __future__ import annotations

# from typing import Any, Dict, List, Tuple
# import pandas as pd

# from src.config.settings import settings
# from src.utils.helpers import write_json
# from src.utils.s3 import upload_file


# def row_to_company_card(row: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
#     name = row.get("Name") or row.get("name") or row.get("Company") or row.get("company")
#     country = row.get("Country") or row.get("country")
#     symbol = row.get("Symbol") or row.get("symbol") or row.get("Ticker") or row.get("ticker")

#     text = "\n".join(
#         [
#             f"Company: {name}",
#             f"Symbol: {symbol}",
#             f"Country: {country}",
#             "",
#             "Fundamentals snapshot:",
#             f"Sales: {row.get('Sales') or row.get('sales')}",
#             f"Profit: {row.get('Profit') or row.get('profit')}",
#             f"Assets: {row.get('Assets') or row.get('assets')}",
#             f"Market Value: {row.get('Market Value') or row.get('market_value')}",
#         ]
#     )

#     metadata = {
#         "company": name,
#         "symbol": symbol,
#         "country": country,
#         "snapshot_date": settings.SNAPSHOT_DATE,
#         "data_type": "fundamentals",
#     }
#     return text, metadata


# def build_company_cards() -> List[Dict[str, Any]]:
#     settings.ensure_dirs()

#     if settings.FUNDAMENTALS_CLEAN_PARQUET.endswith(".parquet"):
#         df = pd.read_parquet(settings.FUNDAMENTALS_CLEAN_PARQUET)
#     else:
#         df = pd.read_csv(settings.FUNDAMENTALS_CSV)

#     cards: List[Dict[str, Any]] = []
#     for _, r in df.iterrows():
#         text, meta = row_to_company_card(r.to_dict())
#         cards.append({"text": text, "metadata": meta})
        
#     return cards


# def write_company_cards_json() -> str:
#     settings.ensure_dirs()
#     cards = build_company_cards()
#     out_path = settings.COMPANY_CARDS_JSON
#     write_json(out_path, cards)
#     upload_file(out_path)

#     return out_path

from __future__ import annotations

from typing import Dict, Tuple, Any

import pandas as pd
from pathlib import Path
from src.utils.helpers import safe_json_dump

from src.config.settings import settings




def row_to_company_card(row: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    text = "\n".join(
        [
            f"Company: {row.get('Name')}",
            f"Country: {row.get('Country')}",
            "",
            f"Financial snapshot ({settings.SNAPSHOT_DATE}):",
            f"Sales: {row.get('Sales')}",
            f"Profit: {row.get('Profit')}",
            f"Assets: {row.get('Assets')}",
            f"Market Value: {row.get('Market Value')}",
        ]
    )

    metadata = {
        "company": str(row.get("Name", "")).strip(),
        "country": str(row.get("Country", "")).strip(),
        "snapshot_date": str(settings.SNAPSHOT_DATE),
        "data_type": "fundamentals",
    }
    return text, metadata


def build_company_cards(csv_path: str | None = None):

    settings.ensure_dirs()

    # if settings.FUNDAMENTALS_CLEAN_PARQUET.endswith(".parquet"):
    #     df = pd.read_parquet(settings.FUNDAMENTALS_CLEAN_PARQUET)
    # else:
    #     df = pd.read_csv(settings.FUNDAMENTALS_CSV)

    clean_path = Path(settings.FUNDAMENTALS_CLEAN_PARQUET)

    if clean_path.exists():
        df = pd.read_parquet(clean_path)
    else:
        df = pd.read_csv(settings.FUNDAMENTALS_CSV)

    # path = settings.fundamentals_csv_path if csv_path is None else csv_path
    # df = pd.read_csv(path)
    docs = [row_to_company_card(r.to_dict()) for _, r in df.iterrows()]

    texts = [t for t, _ in docs]
    metadatas = [m for _, m in docs]

    return texts, metadatas


def write_company_cards_json(texts, metadatas) -> str:
    settings.ensure_dirs()
    # texts, metadatas = build_company_cards()
    out_path = Path(settings.COMPANY_CARDS_JSON)

    docs = [{"text": t, "metadata": m} for t, m in zip(texts, metadatas)]
    safe_json_dump(out_path, docs)

    return str(out_path)