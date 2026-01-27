from __future__ import annotations

# from fastapi import APIRouter
# from src.api.schemas import QueryRequest, QueryResponse
# from src.agent.graph import run_agent

# router = APIRouter()


# @router.post("/query", response_model=QueryResponse)
# def query(req: QueryRequest) -> QueryResponse:
#     result = run_agent(req.question)

#     return QueryResponse(answer = result.get("answer", ""), symbol = result.get("answer"),)


from fastapi import APIRouter

from src.api.schemas import AskRequest, AskResponse
from src.agent.graph import run_agent

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    out = run_agent(req.question)
    return AskResponse(answer=out)
