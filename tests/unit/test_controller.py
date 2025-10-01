import pytest
from src.controller import Controller

# session = MagicMock()
# session.execute.return_value.scalars.return_value.all.return_value = [
#     Task(
#         task_id=1,
#         task_name="Test",
#         user_id=123,
#         status=TaskStatus.PENDING,
#         due_date=date(2025, 9, 30),
#         priority=TaskPriority.HIGH
#     ),
#     Task(
#         task_id=2,
#         task_name="Test2",
#         user_id=456,
#         status=TaskStatus.COMPLETED,
#         due_date=date(2025, 10, 1),
#         priority=TaskPriority.LOW
#     )
# ]