# from __future__ import annotations

# from typing import Any, Dict, List, Optional

# from langchain_openai import ChatOpenAI

# from src.agent.prompts import SYSTEM_PROMPT
# from src.agent.state import AgentState
# from src.config.settings import settings
# from src.tools.retrieve_context import retrieve_context
# from src.tools.fetch_news import fetch_news
# from src.tools.fetch_prices import fetch_prices


# def _guess_symbol(question: str) -> Optional[str]:
#     q = question.upper()
#     for t in settings.tickers_list():
#         if t in q:
#             return t
#     return None


# def _format_context(retrieved: List[Dict[str, Any]]) -> str:
#     parts = []
#     for r in retrieved:
#         meta = r.get("metadata", {}) or {}
#         parts.append(f"Metadata: {meta}\nText:\n{r.get('text','')}")
#     return "\n\n---\n\n".join(parts)


# def run_agent(question: str) -> Dict[str, Any]:
#     settings.ensure_dirs()

#     state: AgentState = {"question": question}

#     symbol = _guess_symbol(question)
#     state["symbol"] = symbol

#     retrieved = retrieve_context(question)
#     state["retrieved"] = retrieved

#     if symbol:
#         state["news"] = fetch_news(symbol, allow_live_fallback=True)
#         state["prices"] = fetch_prices(symbol, allow_live_fallback=True)
#     else:
#         state["news"] = []
#         state["prices"] = {}

#     ctx = _format_context(retrieved)
#     news = state.get("news", [])
#     prices = state.get("prices", {})

#     user_prompt = f"""
#                 Question:
#                 {question}

#                 Retrieved fundamentals context:
#                 {ctx}

#                 Price info:
#                 {prices}

#                 Recent news items:
#                 {news}
#                 """

#     llm = ChatOpenAI(
#         api_key=settings.OPENAI_API_KEY,
#         model=settings.OPENAI_CHAT_MODEL,
#         temperature=0.2,
#     )

#     msg = llm.invoke(
#         [
#             {"role": "system", "content": SYSTEM_PROMPT.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ]
#     )

#     state["answer"] = msg.content
#     return dict(state)



# from __future__ import annotations

# from typing import Any, Dict

# from langgraph.graph import StateGraph, END

# from src.agent.state import AgentState, NextStep
# from src.tools.retrieve_context import retrieve_context
# from src.agent.prompts import generate_answer
# from src.config.settings import settings
# from src.data_access.market_store import MarketStore
# from src.data_access.news_store import NewsStore
# from src.data_access.finnhub_store import FinnhubStore

# # _settings = get_settings()

# _market_store = MarketStore()
# _news_store = NewsStore()
# _finnhub_store = FinnhubStore()


# def node_plan(state: AgentState) -> AgentState:
#     if not state.retrieved:
#         state.next_step = "retrieve"
#         return state
#     if not state.quotes and not state.profiles:
#         state.next_step = "market"
#         return state
#     if not state.news:
#         state.next_step = "news"
#         return state
#     state.next_step = "final"
#     return state


# def node_retrieve(state: AgentState) -> AgentState:
#     state.retrieved = retrieve_context(state.question)
#     return state


# def node_market(state: AgentState) -> AgentState:
#     tickers = settings.tickers_list

#     market_bundle = _market_store.get_market_bundle(tickers)
#     finnhub_bundle = _finnhub_store.get_finnhub_bundle(tickers)

#     m_payload = market_bundle.get("payload") or {}
#     f_payload = finnhub_bundle.get("payload") or {}

#     state.quotes = (m_payload.get("quotes") or []) + (f_payload.get("quotes") or [])
#     state.profiles = (m_payload.get("profiles") or []) + (f_payload.get("profiles") or [])

#     state.market_errors = (m_payload.get("errors") or []) + (f_payload.get("errors") or [])

#     state.served_from["market"] = {
#         "market_store": {"served_from": market_bundle.get("served_from"), "artifact_generated_at": market_bundle.get("artifact_generated_at")},
#         "finnhub_store": {"served_from": finnhub_bundle.get("served_from"), "artifact_generated_at": finnhub_bundle.get("artifact_generated_at")},
#     }
#     return state


# def node_news(state: AgentState) -> AgentState:
#     bundle = _news_store.get_news_bundle(state.question)
#     payload = bundle.get("payload") or {}
#     state.news = payload.get("items") or []
#     state.served_from["news"] = {"served_from": bundle.get("served_from"), "artifact_generated_at": bundle.get("artifact_generated_at")}
#     return state


# def node_final(state: AgentState) -> AgentState:
#     state.answer = generate_answer(
#         question=state.question,
#         retrieved=state.retrieved,
#         quotes=state.quotes,
#         profiles=state.profiles,
#         news=state.news,
#         market_errors=state.market_errors,
#         served_from=state.served_from,
#     )
#     return state


# def build_graph():
#     g = StateGraph(AgentState)
#     g.add_node("plan", node_plan)
#     g.add_node("retrieve", node_retrieve)
#     g.add_node("market", node_market)
#     g.add_node("news", node_news)
#     g.add_node("final", node_final)

#     g.set_entry_point("plan")

#     def route(state: AgentState) -> NextStep:
#         return state.next_step or "final"

#     g.add_conditional_edges("plan", route, {"retrieve": "retrieve", "market": "market", "news": "news", "final": "final"})
#     g.add_edge("retrieve", "plan")
#     g.add_edge("market", "plan")
#     g.add_edge("news", "plan")
#     g.add_edge("final", END)

#     return g.compile()


# agent_graph = build_graph()


# def run_agent(question: str) -> Dict[str, Any]:
#     final = agent_graph.invoke(AgentState(question=question))
#     return final.answer or {}



from __future__ import annotations

from typing import Any, Dict

from langgraph.graph import StateGraph, END

from agent.state import AgentState, NextStep
from tools.retrieve_context import retrieve_context
from agent.prompts import generate_answer
from config.settings import settings

# WIRED TOOLS (agent calls tools only)
from tools.fetch_market_bundle import fetch_market_bundle
from tools.fetch_news import fetch_news


def node_plan(state: AgentState) -> AgentState:
    if not state.retrieved:
        state.next_step = "retrieve"
        return state
    if not state.quotes and not state.profiles:
        state.next_step = "market"
        return state
    if not state.news:
        state.next_step = "news"
        return state
    state.next_step = "final"
    return state


def node_retrieve(state: AgentState) -> AgentState:
    state.retrieved = retrieve_context(state.question)
    return state


def node_market(state: AgentState) -> AgentState:
    # FIX: tickers_list is a method
    tickers = settings.tickers_list()

    bundle = fetch_market_bundle(tickers)
    payload = bundle.get("payload") or {}

    state.quotes = payload.get("quotes") or []
    state.profiles = payload.get("profiles") or []
    state.market_errors = payload.get("errors") or []

    state.served_from["market"] = {
        "served_from": bundle.get("served_from"),
        "artifact_generated_at": bundle.get("artifact_generated_at"),
    }
    return state


def node_news(state: AgentState) -> AgentState:
    bundle = fetch_news(state.question)
    payload = bundle.get("payload") or {}

    state.news = payload.get("items") or []
    state.served_from["news"] = {
        "served_from": bundle.get("served_from"),
        "artifact_generated_at": bundle.get("artifact_generated_at"),
    }
    return state


def node_final(state: AgentState) -> AgentState:
    state.answer = generate_answer(
        question=state.question,
        retrieved=state.retrieved,
        quotes=state.quotes,
        profiles=state.profiles,
        news=state.news,
        market_errors=state.market_errors,
        served_from=state.served_from,
    )
    return state


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("plan", node_plan)
    g.add_node("retrieve", node_retrieve)
    g.add_node("market", node_market)
    g.add_node("news", node_news)
    g.add_node("final", node_final)

    g.set_entry_point("plan")

    def route(state: AgentState) -> NextStep:
        return state.next_step or "final"

    g.add_conditional_edges(
        "plan",
        route,
        {"retrieve": "retrieve", "market": "market", "news": "news", "final": "final"},
    )

    g.add_edge("retrieve", "plan")
    g.add_edge("market", "plan")
    g.add_edge("news", "plan")
    g.add_edge("final", END)

    return g.compile()


agent_graph = build_graph()


# def run_agent(question: str) -> Dict[str, Any]:
#     final = agent_graph.invoke(AgentState(question=question))

#     return final.answer or {}

def run_agent(question: str) -> Dict[str, Any]:
    final = agent_graph.invoke(AgentState(question=question))

    # If LangGraph returns a dict
    if isinstance(final, dict):
        return final.get("answer") or {}

    # If it returns AgentState (older behavior)
    return getattr(final, "answer", None) or {}

