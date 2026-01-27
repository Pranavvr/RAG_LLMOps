# from __future__ import annotations

# from pathlib import Path
# import shutil
# from typing import Any, Dict, List, Optional

# # from langchain_chroma import Chroma
# from langchain_community.vectorstores import Chroma

# from src.config.settings import settings

# from src.embeddings.embedder import get_embedder


# _VECTORSTORE: Optional[Chroma] = None


# # def build_chroma_from_cards(
# #     cards: List[Dict[str, Any]],
# #     rebuild: bool = True,
# #     collection_name: str = "company_cards",
# # ) -> str:
    
# #     settings.ensure_dirs()

# #     persist_dir = Path(settings.CHROMA_PERSIST_DIR)
# #     persist_dir.mkdir(parents=True, exist_ok=True)

# #     if rebuild:
# #         for child in persist_dir.glob("*"):
# #             if child.is_file():
# #                 child.unlink()
# #             else:
# #                 import shutil
# #                 shutil.rmtree(child, ignore_errors=True)

# #     emb = get_embedder()

# #     vs = Chroma(
# #         collection_name=collection_name,
# #         persist_directory=str(persist_dir),
# #         embedding_function=emb,
# #     )

# #     texts = [c["text"] for c in cards]
# #     metadatas = [c["metadata"] for c in cards]
# #     ids = [f"company::{(m.get('symbol') or m.get('company') or '')}".strip() for m in metadatas]

# #     vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)
# #     vs.persist()

# #     return str(persist_dir)


# def build_chroma_from_cards(
#     cards: List[Dict[str, Any]],
#     # texts,
#     # metadatas,
#     # chroma_dir,
#     collection_name="company_cards",
#     rebuild: bool=False,
#     # embed_model="text-embedding-3-large",
#     # openai_api_key=None,
# ):
#     # if not openai_api_key:
#     #     raise ValueError("OPENAI_API_KEY is missing")

#     p = Path(settings.CHROMA_PERSIST_DIR) #Path(chroma_dir)

#     if rebuild and p.exists():
#         shutil.rmtree(p)

#     p.mkdir(parents=True, exist_ok=True)

#     emb = get_embedder()

#     vs = Chroma(
#         collection_name=collection_name,
#         persist_directory=str(p),
#         embedding_function=emb,
#     )

#     texts = [c["text"] for c in cards]
#     metadatas = [c["metadata"] for c in cards]
#     # ids = [f"company::{(m.get('symbol') or m.get('company') or '')}".strip() for m in metadatas]

#     if texts:
#         ids = [f"company::{m.get('company','').strip()}" for m in metadatas]
#         vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

#     vs.persist()
    
#     return vs



# def get_vectorstore(collection_name: str = "company_cards") -> Chroma:
#     global _VECTORSTORE
#     if _VECTORSTORE is not None:
#         return _VECTORSTORE

#     settings.ensure_dirs()
#     emb = get_embedder()
#     _VECTORSTORE = Chroma(
#         collection_name=collection_name,
#         persist_directory=str(Path(settings.CHROMA_PERSIST_DIR)),
#         embedding_function=emb,
#     )
#     return _VECTORSTORE




from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.vectorstores import Chroma

from src.config.settings import settings
from src.embeddings.embedder import get_openai_embedder

# _settings = get_settings()

_VECTORSTORE: Optional[Chroma] = None


def build_chroma_from_company_cards(
    texts: List[str],
    metadatas: List[Dict[str, Any]],
    chroma_dir: Path,
    collection_name: str = "company_cards",
    rebuild: bool = False,
) -> Chroma:
    chroma_dir = Path(chroma_dir)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    if rebuild and chroma_dir.exists():
        shutil.rmtree(chroma_dir)
        chroma_dir.mkdir(parents=True, exist_ok=True)

    emb = get_openai_embedder()

    vs = Chroma(
        collection_name=collection_name,
        persist_directory=str(chroma_dir),
        embedding_function=emb,
    )

    if texts:
        ids = [f"company::{(m.get('company') or '').strip()}" for m in metadatas]
        vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    vs.persist()
    return vs


def get_vectorstore() -> Chroma:
    global _VECTORSTORE
    if _VECTORSTORE is None:
        _VECTORSTORE = build_chroma_from_company_cards(
            texts=[],
            metadatas=[],
            chroma_dir=settings.CHROMA_PERSIST_DIR,
            collection_name="company_cards",
            rebuild=False,
        )
    return _VECTORSTORE
