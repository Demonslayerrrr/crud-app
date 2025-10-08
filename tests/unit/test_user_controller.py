from datetime import datetime
from pydantic import ValidationError
from pytest import raises, fixture
from src.controllers.controller_users import UserController as Controller
from src.repositories.repository_users import UserRepository as Repository
from unittest.mock import Mock
from src.utils.exceptions import NotFound
from src.utils.models import User


@fixture
def repository() -> Mock:
    repository = Mock(spec=Repository)
    return repository

@fixture
def controller(repository: Repository) -> Controller:
    return Controller(repository)

def test_read_users(controller: Controller, repository: Mock) -> None:
    user = User(
        id=1,
        username="test",
        role="test",
        created_at=datetime.now(),
    )
    repository.read.return_value = [user for _ in range(3)]

    result = controller.read()

    assert result == [user for _ in range(3)]

def test_read_users_empty(controller: Controller, repository: Mock) -> None:
    repository.read.return_value = []
    result = controller.read()
    assert result == []

def test_read_user_by_id(controller: Controller, repository: Mock) -> None:
    user = User()
    repository.read_by_id.return_value = user
    result = controller.read_by_id(0)
    assert result == user

def test_read_user_by_id_empty(controller: Controller, repository: Mock) -> None:
    repository.read_by_id.return_value = None
    with raises(NotFound):
        controller.read_by_id(0)

def test_create_user(controller: Controller) -> None:
    data = {
        "id": 1,
        "username": "test",
        "role": "test",
        "created_at": datetime.now()
    }
    controller.create(data)

def test_create_user_invalid(controller: Controller, repository: Mock) -> None:
    data = {
        "id": "a",
        "username": 123,
    }

    with raises(ValidationError):
        controller.create(data)

def test_update_user(controller: Controller, repository: Mock) -> None:
    data = {
        "id" : 1,
        "username": "test",
        "role": "test",
        "created_at": datetime.now()
    }

    controller.update(1,data)

def test_update_user_invalid(controller: Controller, repository: Mock) -> None:
    data = {
        "id": 1,
        "username": 123,
        "role": "test",
        "created_at": datetime.now()
    }

    with raises(ValidationError):
        controller.update(1,data)

def test_delete_user(controller: Controller, monkeypatch) -> None:
    called = {}
    def delete(id: int) -> None:
        called[id] = True

    monkeypatch.setattr(controller, 'delete', delete)

    controller.delete(1)

    assert called[1]

def test_delete_user_not_found_raise(controller: Controller, monkeypatch) -> None:
    def delete(id: int) -> None:
        raise NotFound

    monkeypatch.setattr(controller, 'delete', delete)
    with raises(NotFound):
        controller.delete(1)






