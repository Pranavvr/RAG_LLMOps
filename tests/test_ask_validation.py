from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_ask_missing_body():
    r = client.post("/ask", json={})
    assert r.status_code in (400, 422)

