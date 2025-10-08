from pytest import fixture
from src.repositories.repository_tasks import TasksRepository as Repository
from unittest.mock import Mock
from src.utils.models import Task, TaskStatus, TaskPriority
from datetime import date
from sqlalchemy import Update
from src.settings import settings
from sqlalchemy.orm import scoped_session

@fixture
def mock_session() -> scoped_session:
    return Mock(spec=scoped_session)
@fixture
def repository(mock_session: scoped_session) -> Repository:
    db_url = settings.database_url

    return Repository(url=db_url, session=mock_session)

def test_repository_init(repository: Repository) -> None:
    assert isinstance(repository, Repository)

def test_repository_clear(repository: Repository, mock_session: scoped_session) -> None:
    repository.clear()
    assert mock_session.execute.call_count == 2 and mock_session.commit.call_count == 1

def test_repository_get_tasks(repository: Repository, mock_session: scoped_session) -> None:
    fake_result = Mock()
    fake_scalars = Mock()
    fake_scalars.all.return_value = [Mock(spec=Task), Mock(spec=Task)]
    fake_result.scalars.return_value = fake_scalars
    mock_session.execute.return_value = fake_result

    result = repository.read()

    mock_session.execute.assert_called_once()
    assert len(result) == 2
    assert all(isinstance(i, Task) for i in result)


def test_repository_get_task_by_id(repository: Repository, mock_session: scoped_session) -> None:
    repository.read_by_id(1)
    mock_session.get.assert_called_once_with(Task, 1)


def test_repository_delete(repository: Repository, mock_session: scoped_session) -> None:
    repository.delete(1)
    mock_session.execute.assert_called_once
    mock_session.commit.assert_called_once

def test_repository_update(repository: Repository, mock_session: scoped_session) -> None:
    repository.update(1, new_task_name="c", new_user_id=0, new_status=TaskStatus.PENDING, new_due_date=date.today(), new_priority=TaskPriority.LOW)
    mock_session.execute.assert_called_once
    args, _= mock_session.execute.call_args
    assert isinstance(args[0], Update)
    mock_session.commit.assert_called_once()