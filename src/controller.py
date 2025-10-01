from src.repository import Repository
from models import Task

class Controller:
    def __init__(self, repository:Repository) -> None:
        self.repository = repository

    def create_task(self) -> None:
        pass

    def read_task(self) -> Task:
        pass

    def update_task(self) -> None:
        pass

    def delete_task(self) -> None:
        pass