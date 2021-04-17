from flask import render_template, request, redirect, url_for

from modules import app
from modules.ctrla import ToDoDB
from modules.model import Task, Folder

task_db = ToDoDB()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form["folder_name"]
        color = request.form["color"]
        task_db.create_one(Folder(name, color=color))

    return render_template("index.html", folders=task_db.get_all(Folder))


@app.route("/folder", methods=["POST", "GET"])
def folder_items():
    id_: int = request.args.get("id_")
    folder: Folder = task_db.find_by_id(Folder, id_)

    if request.method == "POST":
        task_title = request.form["task_title"]
        task_notes = request.form["task_notes"]
        priority = request.form["priority"]

        folder.add_task(Task(task_title, notes=task_notes, priority=priority))

    return render_template("folder_items.html", folder=folder)


@app.route("/delete")
def delete_folder():
    id_: int = request.args.get("id_")
    task_db.delete_one(task_db.find_by_id(Folder, id_))

    return redirect(url_for("index"))


@app.route("/sort")
def sort():
    order_by = request.args.get("order_by")

    return render_template("index.html", tasks=task_db.get_all(Task, order_by=order_by))


@app.route("/mark_done")
def mark_done():
    id_ = int(request.args.get("id_"))
    _: Task = task_db.find_by_id(Task, id_)
    _.toggle_done(True)

    return redirect(url_for("folder_items", id_=_.folders.id))
