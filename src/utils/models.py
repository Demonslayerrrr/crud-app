from sqlalchemy import VARCHAR, INT, DATE, DATETIME, Enum as SQLEnum, Column
from sqlalchemy.orm import declarative_base
from src.utils.schemas import TaskStatus, TaskPriority

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(INT, primary_key=True,nullable=False,autoincrement=True)
    username = Column(VARCHAR(30), nullable=False)
    role= Column(VARCHAR(30))
    created_at= Column(DATETIME)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at,
        }

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(INT, primary_key=True,nullable=False,autoincrement=True)
    task_name= Column(VARCHAR(30), nullable=False)
    user_id= Column(INT, nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    due_date= Column(DATE)
    priority = Column(SQLEnum(TaskPriority), nullable=False)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "user_id": self.user_id,
            "status": self.status.value if self.status else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority.value if self.priority else None,
        }