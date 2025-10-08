from abc import ABC, abstractmethod
from src.repositories.repository_tasks import TasksRepository
from src.repositories.repository_users import UserRepository
from src.utils.models import Task, User


class ControllerInterface(ABC):
    def __init__(self, repository: TasksRepository | UserRepository) -> None:
        self.repository = repository

    @abstractmethod
    def create(self, model: Task | User) -> None:
        pass

    @abstractmethod
    def read(self) -> list[Task] | list[User]:
        pass

    @abstractmethod
    def read_by_id(self, id:int) -> Task | User:
        pass

    @abstractmethod
    def update(self, id:int, data:dict) -> None:
        pass

    @abstractmethod
    def delete(self, id:int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
