from __future__ import annotations

from typing import Any, Dict, List
from config.settings import settings
from vectorstore.chroma_store import get_vectorstore


# def retrieve_companies(query: str, k: int | None = None) -> List[Dict[str, Any]]:
#     k = k or settings.RETRIEVAL_TOP_K
#     vs = get_vectorstore()
#     docs = vs.similarity_search(query=query, k=k)

#     out: List[Dict[str, Any]] = []
#     for d in docs:
#         out.append({"text": d.page_content, "metadata": dict(d.metadata or {})})
#     return out


def retrieve_companies(query, k=6):
    k = k or settings.RETRIEVAL_TOP_K
    vs = get_vectorstore()

    results = vs.similarity_search(
        query,
        k=k,
        filter={
            "$and": [
                {"snapshot_date": settings.SNAPSHOT_DATE},
                {"data_type": "fundamentals"},
            ]
        },
    )

    return [
        {
            "company": r.metadata.get("company"),
            "country": r.metadata.get("country"),
            "card": r.page_content,
        }
        for r in results
    ]
