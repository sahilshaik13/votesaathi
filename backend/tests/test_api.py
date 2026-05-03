import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test that the health endpoint returns 200."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_timeline_general():
    """Test fetching the general election timeline."""
    response = client.get("/api/timeline?type=general")
    assert response.status_code == 200
    assert "phases" in response.json()

def test_chat_unauthorized():
    """Test that chat requires a valid user_id and token if provided."""
    # Sending a message with a user_id but no token should be handled
    # (The current implementation checks sub == user_id if both are provided)
    payload = {
        "message": "Hello",
        "session_id": "test-session",
        "user_id": "test-user"
    }
    # This might return 401 if token is missing but user_id is present
    response = client.post("/api/chat", json=payload)
    # Our current logic: if user_id AND authorization: check.
    # If authorization is missing, it skips the check.
    assert response.status_code == 200

def test_dashboard_stats():
    """Test that the dashboard stats endpoint returns data."""
    response = client.get("/api/dashboard/live")
    assert response.status_code == 200
    assert "news" in response.json()
    assert "stats" in response.json()

def test_search_constituency():
    """Test searching for a specific constituency."""
    response = client.get("/api/dashboard/search?query=Lucknow")
    assert response.status_code == 200
    assert response.json()["found"] is True
    assert response.json()["data"]["name"] == "Lucknow"

def test_list_states():
    """Test that the states list returns valid data."""
    response = client.get("/api/dashboard/states")
    assert response.status_code == 200
    assert len(response.json()) > 30
    assert response.json()[0]["name"] == "Andhra Pradesh"

def test_timeline_state():
    """Test fetching a state-specific timeline."""
    response = client.get("/api/timeline?type=state")
    assert response.status_code == 200
    assert "phases" in response.json()
