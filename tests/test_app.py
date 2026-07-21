import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email(client):
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_participant(client):
    response = client.delete("/activities/Chess Club/signup?email=unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
