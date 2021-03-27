from flask import render_template, redirect, request

from modules import app, db
from modules.ctrla import TaskDB
from modules.model import Task

task_db = TaskDB()


@app.route("/")
def index(criterion=None):
    stuff = task_db.get_all(criterion)
    for i in stuff: db.session.refresh(i)
    return render_template("index.html", tasks=task_db.get_all(criterion))


@app.route("/task/<id_>")
def task_pg(id_: int):
    task: Task = task_db.find_by_id(id_)
    return render_template("task_pg.html", task=task)


@app.route("/add", methods=["POST", "GET"])
def add_pg():
    if request.method == "POST":
        title = request.form["title"]
        notes = request.form["notes"]
        priority = request.form["priority"]

        _ = Task(title, notes=notes, priority=priority)
        _.create()

    return render_template("add_pg.html")


@app.route("/delete/<id_>")
def delete(id_: int):
    task_db.delete(id_)
    return redirect("index.html")


@app.route("/sort-priority")
def sort_by_priority():
    return index(criterion=Task.priority)


@app.route("/sort-date_added")
def sort_by_date_added():
    return index(criterion=Task.date_added)
