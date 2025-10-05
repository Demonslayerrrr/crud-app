from flask import Flask, request, jsonify
from http import HTTPStatus

from pydantic import ValidationError

from src.settings import settings
from src.settings import Settings
from src.controller import Controller
from src.repository import Repository
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from src.utils.exceptions import NotFound
from src.utils.models import Base


class AppFlask(Flask):
    def __init__(self, import_name, settings: Settings, *args, **kwargs) -> None:
        super().__init__(import_name, *args, **kwargs)
        self._settings = settings
        self._session = None
        self.repository = None
        self.controller = None


def create_app(settings: Settings) -> AppFlask:
    app = AppFlask(__name__, settings=settings)

    engine = create_engine(settings.database_url)
    session = scoped_session(sessionmaker(bind=engine))
    app._session = session
    app.repository = Repository(settings.database_url, session)
    app.controller = Controller(app.repository)
    Base.metadata.create_all(engine)
    Base.query = session.query_property()


    @app.post("/create")
    def create():
        request_data = request.get_json()
        try:
            app.controller.create_task(request_data)
            return jsonify({"message": "Task was created"}), HTTPStatus.CREATED
        except ValidationError as e:
            return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    @app.get("/tasks")
    def get_tasks():
        result = app.controller.read_tasks()
        return jsonify([task.to_dict() for task in result]), HTTPStatus.OK

    @app.get("/tasks/<int:task_id>")
    def get_task_by_id(task_id: int):
        try:
            task = app.controller.read_task_by_id(task_id)
            return jsonify(task.to_dict()), HTTPStatus.OK
        except NotFound:
            return jsonify({"message": "Task not found"}), HTTPStatus.NOT_FOUND

    @app.patch("/tasks/<int:task_id>")
    def patch_task(task_id: int):
        try:
            new_task = request.get_json()
            app.controller.update_task(task_id, new_task)
            return jsonify({"message": "Task was updated"}), HTTPStatus.OK
        except ValidationError as e:
            return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        try:
            app.controller.delete_task(task_id)
            return jsonify({"message": "Task was deleted"}), HTTPStatus.OK
        except NotFound as e:
            return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    @app.post("/clear")
    def clear():
        app.controller.clear_tasks()
        return jsonify({"message": "Task was cleared"}), HTTPStatus.OK

    return app

if __name__ == "__main__":
    app = create_app(settings)
    app.run(host="localhost", port=8080, debug=True)
