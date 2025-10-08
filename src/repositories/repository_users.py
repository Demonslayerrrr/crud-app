from sqlalchemy import select, text, update
from sqlalchemy.orm import scoped_session
from typing import List, cast, Optional
from src.repositories.repository_interface import RepositoryInterface
from src.utils.models import User

class UserRepository(RepositoryInterface):
    def __init__(self, url:str, session:scoped_session) -> None:
        super().__init__(url, session)

    def create(self, user: User) -> None:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

    def read(self) -> List[User]:
        return cast(List[User],self._session.execute(select(User)).scalars().all())

    def read_by_id(self, id: int) -> Optional[User]:
        return self._session.get(User, id)

    def update(self, id:int, **kwargs) -> None:
        stmt = (
            update(User)
            .where(User.id == id)
            .values(
                username=kwargs["new_username"],
                role=kwargs["new_role"],
                created_at=kwargs["new_created_at"],
            )
        )
        self._session.execute(stmt)
        self._session.commit()

    def delete(self, id:int) -> None:
        self._session.execute(text(f"DELETE FROM users WHERE id = {id}"))
        self._session.commit()

    def clear(self) -> None:
        self._session.execute(text("DELETE FROM users"))
        self._session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        self._session.commit()
