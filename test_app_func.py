# test_app.py

import json
import pytest
from app import app, load_local_facts, FACTS_FILE, USE_API

def test_load_local():
    facts = load_local_facts()
    assert isinstance(facts, list)
    if FACTS_FILE.exists():
        assert len(facts) > 0

def test_random_fact_endpoint():
    client = app.test_client()
    response = client.get("/api/random-fact")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "fact" in data
    assert "source" in data

def test_local_fallback(monkeypatch):
    monkeypatch.setattr("app.USE_API", False)
    
    client = app.test_client()
    response = client.get("/api/random-fact")
    
    if load_local_facts(): 
        assert response.status_code == 200
        data = response.get_json()
        assert data["source"] == "local"
        assert data["fact"] in load_local_facts()
    else:  
        assert response.status_code == 500
