from sqlalchemy import select, text, update
from sqlalchemy.orm import scoped_session
from typing import List, cast, Optional
from src.utils.models import Task
from src.repositories.repository_interface import RepositoryInterface

class TasksRepository(RepositoryInterface):
    def __init__(self, url:str, session:scoped_session) -> None:
        super().__init__(url, session)

    def create(self, task: Task) -> None:
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)

    def read(self) -> List[Task]:
        return cast(List[Task],self._session.execute(select(Task)).scalars().all())

    def read_by_id(self, id: int) -> Optional[Task]:
        return self._session.get(Task, id)

    def update(self, id, **kwargs) -> None:
        stmt = (
            update(Task)
            .where(Task.task_id == id)
            .values(
                task_name=kwargs["new_task_name"],
                user_id=kwargs["new_user_id"],
                status=kwargs["new_status"],
                due_date=kwargs["new_due_date"],
                priority=kwargs["new_priority"],
            )
        )
        self._session.execute(stmt)
        self._session.commit()

    def delete(self, id) -> None:
        self._session.execute(text(f"DELETE FROM tasks WHERE task_id = {id}"))
        self._session.commit()

    def clear(self) -> None:
        self._session.execute(text("DELETE FROM tasks"))
        self._session.execute(text("ALTER SEQUENCE tasks_task_id_seq RESTART WITH 1"))
        self._session.commit()
