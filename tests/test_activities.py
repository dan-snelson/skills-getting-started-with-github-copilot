from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_list_participant():
    email = "testuser@example.com"
    activity = "Basketball"

    # Ensure not already signed up (ignore if already present)
    client.delete(f"/activities/{activity}/participants/{email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant appears in activity list
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email in data[activity]["participants"]


def test_delete_participant():
    email = "remove_me@example.com"
    activity = "Tennis Club"

    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")

    # Now remove them
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Ensure they are gone
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]["participants"]


def test_delete_nonexistent_participant():
    resp = client.delete("/activities/Drama Club/participants/nonexistent@example.com")
    assert resp.status_code == 404


def test_delete_nonexistent_activity():
    resp = client.delete("/activities/NoSuchClub/participants/someone@example.com")
    assert resp.status_code == 404
