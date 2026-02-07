from __future__ import annotations

import sys
from agent.graph import run_agent


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m src.cli.run_query \"your question\"")
        raise SystemExit(1)

    question = sys.argv[1]
    result = run_agent(question)

    print(result.get("answer", ""))
    print("\n")
    if result.get("symbol"):
        print("Symbol:", result["symbol"])
    print("Retrieved:", len(result.get("retrieved", [])))


if __name__ == "__main__":
    main()
