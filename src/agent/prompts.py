# from __future__ import annotations

# SYSTEM_PROMPT = """
# You are a Smart Investor assistant.
# Use retrieved fundamentals context plus news and price snapshot to answer.
# If recent news is missing, say so.
# Be clear, practical, and investor oriented.
# """


from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from config.settings import settings

# _settings = get_settings()


class CompanyOut(BaseModel):
    company: str
    ticker: Optional[str] = None
    why_relevant: str


class KeyNumbersOut(BaseModel):
    company: str
    sales: Optional[str] = None
    profit: Optional[str] = None
    assets: Optional[str] = None
    market_value: Optional[str] = None


class AnswerOut(BaseModel):
    summary: str
    companies: List[CompanyOut] = Field(default_factory=list)
    bull_points: List[str] = Field(default_factory=list)
    bear_points: List[str] = Field(default_factory=list)
    key_numbers: List[KeyNumbersOut] = Field(default_factory=list)
    data_notes: List[str] = Field(default_factory=list)


SYSTEM_PROMPT = """You are a helpful financial analyst assistant.

                You have:
                Retrieved company fundamentals context cards (Sales, Profit, Assets, Market Value) for a fixed snapshot year.
                Optional market quotes and profiles from cached snapshots or live calls.
                Optional recent news snippets from cached snapshots or live calls.

                Rules:
                Be clear that fundamentals are a snapshot for SNAPSHOT_DATE.
                Do not hallucinate numbers.
                If something is missing, say unknown.
                Prefer bullet points and practical investor style writing.
                """


def get_llm_structured() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.OPENAI_CHAT_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.2,
    ).with_structured_output(AnswerOut)


def generate_answer(
    question: str,
    retrieved: List[Dict[str, Any]],
    quotes: List[Dict[str, Any]],
    profiles: List[Dict[str, Any]],
    news: List[Dict[str, Any]],
    market_errors: List[Dict[str, Any]],
    served_from: Dict[str, Any],
) -> Dict[str, Any]:
    llm = get_llm_structured()

    payload = {
        "question": question,
        "snapshot_date": settings.SNAPSHOT_DATE,
        "retrieved_cards": retrieved,
        "quotes": quotes,
        "profiles": profiles,
        "news": news,
        "market_errors": market_errors,
        "served_from": served_from,
    }

    return llm.invoke(
        [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": str(payload)}]
    ).model_dump()
