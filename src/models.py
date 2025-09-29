from sqlalchemy import VARCHAR,INT,DATETIME, Enum as SQLEnum
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in-progress'
    COMPLETED = 'completed'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(INT, primary_key=True,nullable=False,autoincrement=True)
    username:Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    role:Mapped[str] = mapped_column(VARCHAR(30))
    created_at:Mapped[datetime] = mapped_column(DATETIME)
    def __repr__(self):
        return f'<User id: {self.id} username: {self.username} role: {self.role} created_at: {self.created_at}>'

class Task(Base):
    __tablename__ = 'tasks'
    task_id:Mapped[int] = mapped_column(INT, primary_key=True,nullable=False,autoincrement=True)
    task_name:Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    user_id:Mapped[int] = mapped_column(VARCHAR(30), nullable=False)
    status:Mapped[TaskStatus] = mapped_column(SQLEnum('pending', 'in-progress', 'completed'))
    due_date:Mapped[datetime] = mapped_column(DATETIME)
    priority:Mapped[TaskPriority] = mapped_column(SQLEnum('low', 'medium', 'high'))