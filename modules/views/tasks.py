import datetime

from flask import render_template, url_for, request, session, Blueprint
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import db
from modules.model import Task, Folder

tasks = Blueprint("tasks", __name__)


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
    name = request.form["name"]
    folder = request.form["folder"]
    reminder: bool = request.form.get("reminder") is not None
    date_due = request.form["date_due"] if reminder else None

    _ = Task(name=name.title(),
             folder=int(folder),
             reminder=reminder,
             date_due=date_due,
             date_created=datetime.datetime.now())

    db.session.add(_)
    db.session.commit()

    return redirect(request.referrer)


@tasks.route("/subtask_create", methods=["POST"])
def subtask_create():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    name = request.form["name"].title()
    _.subtasks.append(Task(name=name,
                           date_created=datetime.datetime.now(),
                           folder=_.folder))
    db.session.commit()

    return redirect(request.referrer)


@tasks.route("/task_update", methods=["POST"])
def task_update():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    _.name = request.form["name"]
    _.note = request.form["note"]
    _.folder = int(request.form["folder"])
    _.reminder = request.form.get("reminder") is not None
    _.date_due = request.form["date_due"] if _.reminder else None

    db.session.commit()

    return redirect(request.referrer)


@tasks.route("/task_delete")
def task_delete():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("tasks"))


@tasks.route("/task_toggle")
def task_toggle():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    if not _.done:
        _.done = True
        _.date_done = datetime.datetime.now()
    else:
        _.done = False
        _.date_done = None
    db.session.commit()

    return redirect(request.referrer)


@tasks.route("/hide_toggle")
def hide_toggle():
    if bool(session.get("hide_completed")) is True:
        session["hide_completed"] = False
    else:
        session["hide_completed"] = True

    return redirect(request.referrer)


@tasks.route("/task_clear")
def task_clear():
    db.session.execute("TRUNCATE TABLE tasks")
    db.session.commit()

    return redirect(request.referrer)