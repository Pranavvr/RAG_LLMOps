# from __future__ import annotations

# from typing import Any, Dict, List
# from src.retrieval.retrieve_companies import retrieve_companies


# def retrieve_context(question: str) -> List[Dict[str, Any]]:
#     return retrieve_companies(question)

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.retrieval.retrieve_companies import retrieve_companies


def retrieve_context(question: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
    return retrieve_companies(question, k=k)
