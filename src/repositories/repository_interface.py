from abc import ABC, abstractmethod
from typing import Optional, List
from src.utils.models import Task, User
from sqlalchemy.orm import scoped_session


class RepositoryInterface(ABC):
    def __init__(self, url:str, session:scoped_session) -> None:
        self.db_url = url
        self._session = session

    @abstractmethod
    def create(self, model: Task | User) -> None:
        pass

    @abstractmethod
    def update(self, id:int, **kwargs) -> None:
        pass

    @abstractmethod
    def delete(self, id:int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def read(self) -> List[Task] | List[User]:
        pass

    @abstractmethod
    def read_by_id(self, id:int) -> Optional[Task] | Optional[User]:
        pass