from __future__ import annotations

from langchain_openai import OpenAIEmbeddings
from src.config.settings import settings


def get_openai_embedder() -> OpenAIEmbeddings:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY missing")
    return OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_EMBED_MODEL,
    )


# from __future__ import annotations

# from langchain_openai import OpenAIEmbeddings
# from src.config.settings import get_settings

# _settings = get_settings()


# def get_openai_embedder() -> OpenAIEmbeddings:
#     return OpenAIEmbeddings(
#         model=_settings.OPENAI_EMBED_MODEL,
#         api_key=_settings.OPENAI_API_KEY,
#     )
