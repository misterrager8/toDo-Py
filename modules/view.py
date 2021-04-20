from flask import render_template, request, redirect, url_for

from modules import app
from modules.ctrla import ToDoDB
from modules.model import Task, Folder

task_db = ToDoDB()


@app.route("/", methods=["POST", "GET"])
def index():
    order_by = request.args.get("order_by", default="date_created desc")

    if request.method == "POST":
        name = request.form["folder_name"]
        color = request.form["color"]
        task_db.create_one(Folder(name, color=color))

        return redirect(url_for("index"))

    folders = task_db.get_all(Folder, order_by=order_by)
    return render_template("index.html", folders=folders, order_by=order_by)


@app.route("/folder", methods=["POST", "GET"])
def folder_items():
    order_by = request.args.get("order_by", default="date_added desc")
    id_: int = request.args.get("id_")
    folder: Folder = task_db.find_by_id(Folder, id_)

    if request.method == "POST":
        task_title = request.form["task_title"]
        task_notes = request.form["task_notes"]
        priority = request.form["priority"]

        folder.add_task(Task(task_title, notes=task_notes, priority=priority))

    return render_template("folder_items.html", folder=folder, order_by=order_by)


@app.route("/delete")
def delete_folder():
    id_: int = request.args.get("id_")
    task_db.delete_one(task_db.find_by_id(Folder, id_))

    return redirect(url_for("index", folders=task_db.get_all(Folder)))


@app.route("/delete_task")
def delete_task():
    id_: int = request.args.get("id_")
    order_by = request.args.get("order_by")
    task: Task = task_db.find_by_id(Task, id_)
    folder_id = task.folder_id

    task_db.delete_one(task)

    return redirect(url_for("folder_items", id_=folder_id, order_by=order_by))


@app.route("/toggle_done")
def toggle_done():
    id_ = int(request.args.get("id_"))
    order_by = request.args.get("order_by")
    _: Task = task_db.find_by_id(Task, id_)
    if _.done:
        _.toggle_done(False)
    else:
        _.toggle_done(True)

    return redirect(url_for("folder_items", id_=_.folders.id, order_by=order_by))
