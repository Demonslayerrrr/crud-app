from flask import Flask, request, jsonify
from http import HTTPStatus
from pydantic import ValidationError
from src.controllers.controller_tasks import TaskController
from src.repositories.repository_users import UserRepository
from src.settings import settings
from src.settings import Settings
from src.controllers.controller_users import UserController
from src.repositories.repository_tasks import TasksRepository
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from src.utils.exceptions import NotFound
from src.utils.models import Base


class AppFlask(Flask):
    def __init__(self, import_name, settings: Settings, *args, **kwargs) -> None:
        super().__init__(import_name, *args, **kwargs)
        self._settings = settings
        self._session = None
        self.task_repository = None
        self.user_repository = None
        self.controller_tasks = None
        self.controller_users = None


def create_app(settings: Settings) -> AppFlask:
    app = AppFlask(__name__, settings=settings)

    engine = create_engine(settings.database_url)
    session = scoped_session(sessionmaker(bind=engine))
    app._session = session
    app.task_repository = TasksRepository(settings.database_url, session)
    app.controller_tasks = TaskController(app.task_repository)
    app.user_repository = UserRepository(settings.database_url, session)
    app.controller_users = UserController(app.user_repository)
    Base.metadata.create_all(engine)
    Base.query = session.query_property()


    @app.post("/create_task")
    def create():
        request_data = request.get_json()
        try:
            app.controller_tasks.create(request_data)
            return jsonify({"message": "Task was created"}), HTTPStatus.CREATED
        except ValidationError as e:
            return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    @app.post("/create_user")
    def create_user():
        request_data = request.get_json()
        try:
            app.controller_users.create(request_data)
            return jsonify({"message": "User was created"}), HTTPStatus.CREATED
        except ValidationError as e:
            return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    @app.get("/tasks")
    def get_tasks():
        result = app.controller_users.read()
        return jsonify([task.to_dict() for task in result]), HTTPStatus.OK

    @app.get("/users")
    def get_users():
        result = app.controller_users.read()
        return jsonify([user.to_dict() for user in result]), HTTPStatus.OK

    @app.get("/tasks/<int:task_id>")
    def get_task_by_id(task_id: int):
        try:
            task = app.controller_tasks.read_by_id(task_id)
            return jsonify(task.to_dict()), HTTPStatus.OK
        except NotFound:
            return jsonify({"message": "Task not found"}), HTTPStatus.NOT_FOUND

    @app.get("/users/<int:user_id>")
    def get_user_by_id(user_id: int):
        try:
            user = app.controller_users.read_by_id(user_id)
            return jsonify(user.to_dict()), HTTPStatus.OK
        except NotFound:
            return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

    @app.patch("/tasks/<int:task_id>")
    def patch_task(task_id: int):
        try:
            new_task = request.get_json()
            app.controller_tasks.update(task_id, new_task)
            return jsonify({"message": "Task was updated"}), HTTPStatus.OK
        except ValidationError as e:
            return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    @app.patch("/users/<int:user_id>")
    def patch_user(user_id: int):
        try:
            user = app.controller_users.read_by_id(user_id)
            return jsonify(user.to_dict()), HTTPStatus.OK
        except NotFound:
            return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        try:
            app.controller_tasks.delete(task_id)
            return jsonify({"message": "Task was deleted"}), HTTPStatus.OK
        except NotFound as e:
            return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    @app.delete("/users/<int:user_id>")
    def delete_user(user_id: int):
        try:
            user = app.controller_users.read_by_id(user_id)
            return jsonify(user.to_dict()), HTTPStatus.OK
        except NotFound:
            return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

    @app.post("/clear/tasks")
    def clear():
        app.controller_tasks.clear()
        return jsonify({"message": "Task was cleared"}), HTTPStatus.OK

    @app.post("/clear/users")
    def clear_users():
        app.controller_users.clear()
        return jsonify({"message": "User was cleared"}), HTTPStatus.OK
    return app

if __name__ == "__main__":
    app = create_app(settings)
    app.run(host="localhost", port=8080, debug=True)
