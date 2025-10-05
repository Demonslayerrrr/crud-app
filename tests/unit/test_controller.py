from datetime import datetime
from pydantic import ValidationError
from pytest import raises, fixture
from src.controller import Controller
from src.repository import Repository
from unittest.mock import Mock
from src.utils.exceptions import NotFound
from src.utils.models import Task
from src.utils.schemas import TaskPriority, TaskStatus


@fixture
def repository() -> Mock:
    repository = Mock(spec=Repository)
    return repository

@fixture
def controller(repository: Repository) -> Controller:
    return Controller(repository)

def test_read_tasks(controller: Controller, repository: Mock) -> None:
    task = Task(
        task_id=1,
        task_name="task1",
        user_id=1,
        due_date=datetime.today(),
        priority=TaskPriority.LOW,
        status=TaskStatus.PENDING,
    )
    repository.read.return_value = [task for _ in range(3)]

    result = controller.read_tasks()

    assert result == [task for _ in range(3)]

def test_read_tasks_empty(controller: Controller, repository: Mock) -> None:
    repository.read.return_value = []
    result = controller.read_tasks()
    assert result == []

def test_read_task_by_id(controller: Controller, repository: Mock) -> None:
    task = Task()
    repository.read_by_id.return_value = task
    result = controller.read_task_by_id(0)
    assert result == task

def test_read_task_by_id_empty(controller: Controller, repository: Mock) -> None:
    repository.read_by_id.return_value = None
    with raises(NotFound):
        controller.read_task_by_id(0)

def test_create_task(controller: Controller) -> None:
    data = {
        "task_id" : 1,
        "task_name" : "task1",
        "user_id" : 1,
        "due_date" : "2025-10-02",
        "priority" : "low",
        "status" : "pending",
    }
    controller.create_task(data)

def test_create_task_invalid(controller: Controller, repository: Mock) -> None:
    data = {
        "task_id" : 1,
        "task_name" : 3,
        "priority" : "aaaaaa",
    }

    with raises(ValidationError):
        controller.create_task(data)

def test_update_task(controller: Controller, repository: Mock) -> None:
    data = {
        "task_id" : 1,
        "task_name" : "task1",
        "user_id" : 5,
    }

    controller.update_task(data)

def test_update_task_invalid(controller: Controller, repository: Mock) -> None:
    data = {
        "task_id" : 4,
        "task_name" : 10,
        "user_id" : "5",
    }

    with raises(ValidationError):
        controller.update_task(data)

def test_update_task_key_error(controller: Controller, repository: Mock) -> None:
    data = {
        "id" : 1,
        "task_name" : "task1",
        "user_id" : 1,
    }

    with raises(KeyError):
        controller.update_task(data)

def test_delete_task(controller: Controller, monkeypatch) -> None:
    called = {}
    def delete(id: int) -> None:
        called[id] = True

    monkeypatch.setattr(controller, 'delete_task', delete)

    controller.delete_task(1)

    assert called[1]

def test_delete_task_not_found_raise(controller: Controller, monkeypatch) -> None:
    def delete(id: int) -> None:
        raise NotFound

    monkeypatch.setattr(controller, 'delete_task', delete)
    with raises(NotFound):
        controller.delete_task(1)






