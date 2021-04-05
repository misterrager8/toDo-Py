from flask import render_template, request

from modules import app
from modules.ctrla import TaskDB
from modules.model import Task

task_db = TaskDB()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        title = request.form["task_title"]
        notes = request.form["task_notes"]
        priority = request.form["priority"]
        Task(title, notes=notes, priority=priority).create()

    return render_template("index.html", tasks=task_db.get_all())
