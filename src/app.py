from flask import Flask, current_app, request
from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Task

app = Flask(__name__)
@app.get("/create")
def create(task: Task):
    pass

app.run(host="localhost", port=8080, debug=True)


