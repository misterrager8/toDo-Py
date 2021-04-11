from flask import render_template, request, redirect, url_for
from sqlalchemy import text

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


@app.route("/delete")
def delete_task():
    id_: int = request.args.get("id_")
    task_db.delete(id_)

    return redirect(url_for("index"))


@app.route("/sort")
def sort():
    order_by = request.args.get("order_by")

    return render_template("index.html", tasks=task_db.get_all(criterion=text(order_by)))
