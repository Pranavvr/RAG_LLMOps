# from __future__ import annotations

# from typing import Any, Dict, List, Optional, TypedDict


# class AgentState(TypedDict, total=False):
#     question: str
#     symbol: Optional[str]

#     retrieved: List[Dict[str, Any]]
#     news: List[Dict[str, Any]]
#     prices: Dict[str, Any]

#     answer: str


from __future__ import annotations

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field

NextStep = Literal["retrieve", "market", "news", "final"]


class AgentState(BaseModel):
    question: str
    next_step: Optional[NextStep] = None

    retrieved: List[Dict[str, Any]] = Field(default_factory=list)

    quotes: List[Dict[str, Any]] = Field(default_factory=list)
    profiles: List[Dict[str, Any]] = Field(default_factory=list)
    market_errors: List[Dict[str, Any]] = Field(default_factory=list)

    news: List[Dict[str, Any]] = Field(default_factory=list)

    served_from: Dict[str, Any] = Field(default_factory=dict)

    answer: Optional[Dict[str, Any]] = None
