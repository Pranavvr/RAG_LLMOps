# from fastapi.testclient import TestClient
# from api.app import app

# client = TestClient(app)

# def test_ask_endpoint_basic():
#     r = client.post("/ask", json={"question": "hello"})
#     assert r.status_code == 200

# from fastapi.testclient import TestClient

# import api.routes as routes
# from api.app import app

# client = TestClient(app)

# def test_ask_endpoint_basic(monkeypatch):
#     def fake_run_agent(question: str) -> str:
#         return "stubbed answer"

#     monkeypatch.setattr(routes, "run_agent", fake_run_agent)

#     r = client.post("/ask", json={"question": "hello"})
#     assert r.status_code == 200



from fastapi.testclient import TestClient

import api.routes as routes
from api.app import app

client = TestClient(app)

def test_ask_endpoint_basic(monkeypatch):
    def fake_run_agent(question: str):
        return {"text": "stubbed answer"}

    monkeypatch.setattr(routes, "run_agent", fake_run_agent)

    r = client.post("/ask", json={"question": "hello"})
    assert r.status_code == 200
    assert r.json() == {"answer": {"text": "stubbed answer"}}
