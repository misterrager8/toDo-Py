import datetime

from flask import render_template, request, session, Blueprint
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import db
from modules.ctrla import Database
from modules.model import Task, Folder

tasks = Blueprint("tasks", __name__)
database = Database()


@tasks.route("/tasks")
@tasks.route("/tasks/<int:page>")
def tasks_(page=1):
    order_by = request.args.get("order_by", default="tasks.date_created desc")
    if session.get("hide_completed") is True:
        tasks_list = db.session.query(Task).filter(Task.done == False, Task.parent_task == None).join(Folder).order_by(
            text(order_by)).paginate(page=page, per_page=40)
    else:
        tasks_list = db.session.query(Task).filter(Task.parent_task == None).join(Folder).order_by(Task.done, text(
            order_by)).paginate(page=page,
                                per_page=40)

    return render_template("tasks.html", tasks_=tasks_list, order_by=order_by)


@tasks.route("/task_create", methods=["POST"])
def task_create():
    names = request.form.getlist("name")
    folder = request.form["folder"]

    for i in names:
        database.create(Task(name=i.title(),
                             folder=int(folder),
                             date_created=datetime.datetime.now()))

    return redirect(request.referrer)


@tasks.route("/subtask_create", methods=["POST"])
def subtask_create():
    _: Task = database.get(Task, request.args.get("id_"))

    names = request.form.getlist("name")
    for i in names:
        database.create(Task(name=i.title(),
                             date_created=datetime.datetime.now(),
                             folder=_.folder,
                             parent_task=_.id))

    return redirect(request.referrer)


@tasks.route("/task_update", methods=["POST"])
def task_update():
    _: Task = database.get(Task, request.args.get("id_"))

    _.name = request.form["name"]
    _.note = request.form["note"]
    _.folder = int(request.form["folder"])
    _.reminder = request.form.get("reminder") is not None
    _.date_due = request.form["date_due"] if _.reminder else None

    db.session.commit()

    return redirect(request.referrer)


@tasks.route("/task_delete")
def task_delete():
    _: Task = database.get(Task, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)


@tasks.route("/task_toggle")
def task_toggle():
    _: Task = database.get(Task, request.args.get("id_"))
    _.toggle_done()

    return redirect(request.referrer)


@tasks.route("/hide_toggle")
def hide_toggle():
    session["hide_completed"] = False if bool(session.get("hide_completed")) is True else True

    return redirect(request.referrer)


@tasks.route("/task_clear")
def task_clear():
    database.execute_stmt("TRUNCATE TABLE tasks")

    return redirect(request.referrer)
