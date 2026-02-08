import os

def test_env_var_access(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    assert os.getenv("OPENAI_API_KEY") == "test"
