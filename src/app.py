from flask import Flask
from src.utils.models import Task

app = Flask(__name__)
@app.get("/create")
def create(task: Task):
    pass

app.run(host="localhost", port=8080, debug=True)


