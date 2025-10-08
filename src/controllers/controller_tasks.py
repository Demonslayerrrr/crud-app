from src.repositories.repository_tasks import TasksRepository as Repository
from src.utils.models import Task
from src.utils.schemas import TaskCreate, TaskUpdate
from typing import List
from pydantic import ValidationError
from src.utils.exceptions import NotFound
from src.controllers.controller_interface import ControllerInterface

class TaskController(ControllerInterface):
    def __init__(self, repository: Repository) -> None:
        super().__init__(repository)

    def create(self, task: dict) -> None:
        try:
            data = TaskCreate(**task)
            task = Task(**data.model_dump())
            self.repository.create(task)
        except ValidationError as e:
            raise e

    def read(self) -> List[Task]:
        return self.repository.read()

    def read_by_id(self, task_id: int) -> Task:
        task = self.repository.read_by_id(task_id)
        if task is None:
            raise NotFound
        else:
            return task

    def update(self, id:int,task: dict) -> None:
        try:
            old_task = self.repository.read_by_id(id)
            data = TaskUpdate(**task)
            task = Task(**data.model_dump())
            self.repository.update(id=id,
                                   new_task_name=task.task_name if task.task_name else old_task.task_name,
                                   new_status=task.status if task.status else old_task.status,
                                   new_user_id=task.user_id if task.user_id else old_task.user_id,
                                   new_due_date=task.due_date if task.due_date else old_task.due_date,
                                   new_priority=task.priority if task.priority else old_task.priority)
        except ValidationError as e:
            raise e
    def delete(self, task_id:int) -> None:
        if self.repository.read_by_id(task_id) is None:
            raise NotFound
        self.repository.delete(task_id)

    def clear(self) -> None:
        self.repository.clear()