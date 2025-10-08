from src.repositories.repository_users import UserRepository
from src.utils.models import User
from src.utils.schemas import UserUpdate, UserCreate
from typing import List
from pydantic import ValidationError
from src.utils.exceptions import NotFound
from src.controllers.controller_interface import ControllerInterface

class UserController(ControllerInterface):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(repository)

    def create(self, user: dict) -> None:
        try:
            data = UserCreate(**user)
            user = User(**data.model_dump())
            self.repository.create(user)
        except ValidationError as e:
            raise e

    def read(self) -> List[User]:
        return self.repository.read()

    def read_by_id(self, task_id: int) -> User:
        task = self.repository.read_by_id(task_id)
        if task is None:
            raise NotFound
        else:
            return task

    def update(self, id:int,task: dict) -> None:
        try:
            old_user = self.repository.read_by_id(id)
            data = UserUpdate(**task)
            user = User(**data.model_dump())
            self.repository.update(id=id,
                                   new_username = user.username if user.username else old_user.username,
                                   new_role = user.role if user.role else old_user.role,
                                   new_created_at= user.created_at if user.created_at else old_user.created_at
                                   )
        except ValidationError as e:
            raise e
    def delete(self, id:int) -> None:
        if self.repository.read_by_id(id) is None:
            raise NotFound
        self.repository.delete(id)

    def clear(self) -> None:
        self.repository.clear()