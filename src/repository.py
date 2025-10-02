from sqlalchemy import select, text, update
from sqlalchemy.orm import scoped_session
from typing import List, cast, Optional
from src.utils.models import Task

class Repository:
    def __init__(self, url:str, session:scoped_session) -> None:
        self.db_url = url
        self._session = session

    def create(self, task: Task) -> None:
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)

    def read(self) -> List[Task]:
        return cast(List[Task],self._session.execute(select(Task)).scalars().all())

    def read_by_id(self, id: int) -> Optional[Task]:
        return self._session.get(Task, id)

    def update(self, id, new_task_name, new_user_id, new_status, new_due_date, new_priority) -> None:
        stmt = (
            update(Task)
            .where(Task.task_id == id)
            .values(
                task_name=new_task_name,
                user_id=new_user_id,
                status=new_status,
                due_date=new_due_date,
                priority=new_priority,
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
