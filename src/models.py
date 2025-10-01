from sqlalchemy import VARCHAR, INT, DATE, DATETIME, Enum as SQLEnum, Column
from enum import Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
    id = Column(INT, primary_key=True,nullable=False,autoincrement=True)
    username = Column(VARCHAR(30), nullable=False)
    role= Column(VARCHAR(30))
    created_at= Column(DATETIME)
    def __repr__(self):
        return f'<User id: {self.id} username: {self.username} role: {self.role} created_at: {self.created_at}>'

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(INT, primary_key=True,nullable=False,autoincrement=True)
    task_name= Column(VARCHAR(30), nullable=False)
    user_id= Column(INT, nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    due_date= Column(DATE)
    priority = Column(SQLEnum(TaskPriority), nullable=False)