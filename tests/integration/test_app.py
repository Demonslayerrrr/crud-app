from http import HTTPStatus
from src.app import create_app
from pytest import fixture
from flask.testing import FlaskClient
from src.settings import settings

@fixture
def client() -> FlaskClient:
    app = create_app(settings)
    app.config.update(TESTING=True)
    with app.test_client() as client:
        # push app context so DB/session-bound things work if needed
        with app.app_context():
            yield client

def test_clear_tasks(client: FlaskClient) -> None:
    for i in range(5):
        client.post("/create/task", json={
            "task_name": "a",
            "user_id": i,
            "status": "pending",
            "due_date": "2025-10-02",
            "priority": "high"
        })

    response = client.post("/clear/tasks")
    data = client.get("/tasks")
    assert response.status_code == HTTPStatus.OK
    assert data.get_json() == []

def test_get_tasks(client: FlaskClient) -> None:
    client.post("/clear/tasks")
    for i in range(5):
        client.post("/create_task", json={
            "task_name": "a",
            "user_id": i,
            "status": "pending",
            "due_date": "2025-10-02",
            "priority": "high"
        })
    response = client.get("/tasks")
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK
    assert len(data) == 5
    assert all(i["task_name"] == "a" for i in data)

def test_get_task_by_id(client: FlaskClient) -> None:
    client.post("/clear/tasks")
    for i in range(5):
        client.post("/create_task", json={
            "task_name": "a",
            "user_id": i,
            "status": "pending",
            "due_date": "2025-10-02",
            "priority": "high"
        })

    response = client.get("/tasks/1")
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK
    assert data["task_id"] == 1

def test_update_task(client: FlaskClient) -> None:
    client.post("/clear/tasks")
    for i in range(5):
        client.post("/create_task", json={
            "task_name": "a",
            "user_id": i,
            "status": "pending",
            "due_date": "2025-10-02",
            "priority": "high"
        })
    response = client.patch("/tasks/1", json={
        "task_name": "x",
    })
    data = client.get("/tasks/1").get_json()

    assert response.status_code == HTTPStatus.OK
    assert data["task_name"] == "x"

def test_delete_task(client: FlaskClient) -> None:
    client.post("/clear/tasks")
    for i in range(5):
        client.post("/create_task", json={
            "task_name": "a",
            "user_id": i,
            "status": "pending",
            "due_date": "2025-10-02",
            "priority": "high"
        })

    response = client.delete("/tasks/1")
    data = client.get("/tasks/1").get_json()
    assert response.status_code == HTTPStatus.OK
    assert data["message"] == "Task not found"

def test_create_task(client: FlaskClient) -> None:
    client.post("/clear/tasks")
    client.post("/create_task", json={
        "task_name": "a",
        "user_id": 1,
        "status": "pending",
        "due_date": "2025-10-02",
        "priority": "high"
    })
    response = client.get("/tasks")
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK
    assert data[0]["task_name"] == "a"

def test_create_user(client: FlaskClient) -> None:
    client.post("/clear/users")
    client.post("/create_user", json={
        "username" : "a",
        "role" : "a",
        "created_at": "2025-10-01",
    })
    response = client.get("/users")
    data = response.get_json()
    assert response.status_code == HTTPStatus.OK
    assert data[0]["username"] == "a"

