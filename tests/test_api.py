from fastapi.testclient import TestClient
from raraphsopvt.main import app
from raraphsopvt.config import settings


client = TestClient(app)
headers = {"Authorization": f"Bearer {settings.api_key}"}


def test_api_crud_flow():
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Complete sample backend", "description": "Use FastAPI, repository, and tests."},
        headers=headers,
    )
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Complete sample backend"
    task_id = task["id"]

    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"completed": True},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert missing_response.status_code == 404
