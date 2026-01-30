from __future__ import annotations

from pydantic import BaseModel


    # class QueryRequest(BaseModel):
    #     question: str


    # class QueryResponse(BaseModel):
    #     answer: str
    #     symbol: str | None = None


from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)


class AskResponse(BaseModel):
    answer: dict
