from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Initialize the TestClient
client = TestClient(app)


@pytest.fixture
def random_task_id():
    """Generate a random UUID for testing purposes."""
    return uuid4()


@pytest.mark.skip(reason="Deferring for now.")
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"hi"'


def test_sleepy_task():
    # Test with a valid seconds value
    response = client.post("/tasks/sleepy", json={"seconds": 10})
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["state"] == "PENDING"


def test_fib_task():
    # Test with a valid nthNumber value
    response = client.post("/tasks/fib", json={"nthNumber": 10})
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["state"] == "PENDING"


def test_get_one(random_task_id):
    # Assuming we have a task in the backend, use the random task ID to test.
    response = client.get(f"/tasks/{random_task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(random_task_id)


def test_get_all():
    # Test the retrieval of all tasks
    response = client.get("/tasks?sort=id&order=ASC")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
