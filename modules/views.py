import datetime
import random

from flask import request, render_template, current_app, url_for
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from modules import login_manager, db
from modules.ctrla import Database
from modules.models import Folder, Task, User

database = Database()


@login_manager.user_loader
def load_user(id_) -> User:
    _: User = database.get(User, id_)
    return _


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    _ = current_user.folders.order_by(text(order_by))
    return render_template("index.html", folders_=_, order_by=order_by)


@current_app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = db.session.query(User).filter(User.email == email).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("index"))
    else:
        return "Login failed."


@current_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@current_app.route("/signup", methods=["POST"])
def signup():
    database.create(User(first_name=request.form["first_name"],
                         last_name=request.form["last_name"],
                         email=request.form["email"],
                         password=generate_password_hash(request.form["password"]),
                         date_joined=datetime.datetime.now()))

    return redirect(url_for("index"))


@current_app.route("/folder")
@login_required
def folder():
    _: Folder = database.get(Folder, request.args.get("id_"))
    return render_template("folder.html", folder=_)


@current_app.route("/folder_create", methods=["POST"])
@login_required
def folder_create():
    database.create(Folder(name=request.form["name"],
                           color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                           date_created=datetime.datetime.now(),
                           user=current_user.id))

    return redirect(request.referrer)


@current_app.route("/folder_edit", methods=["POST"])
@login_required
def folder_edit():
    _: Folder = database.get(Folder, int(request.form["id_"]))

    _.name = request.form["name"]
    _.color = request.form["color"]
    database.update()

    return redirect(request.referrer)


@current_app.route("/folder_delete")
@login_required
def folder_delete():
    _: Folder = database.get(Folder, request.args.get("id_"))
    for i in _.tasks:
        database.delete(i)
    database.delete(_)

    return redirect(url_for("index"))


@current_app.route("/tasks")
@login_required
def tasks_():
    order_by = request.args.get("order_by", default="tasks.date_created desc")
    _ = current_user.tasks.join(Folder).order_by(text(order_by))
    return render_template("tasks.html", tasks_=_, order_by=order_by)


@current_app.route("/task")
@login_required
def task():
    _: Task = database.get(Task, request.args.get("id_"))

    return render_template("task.html", task=_)


@current_app.route("/task_create", methods=["POST"])
@login_required
def task_create():
    database.create(Task(name=request.form["name"],
                         folder=int(request.form["id_"]),
                         date_created=datetime.datetime.now(),
                         user=current_user.id))

    return redirect(request.referrer)


@current_app.route("/subtask_create", methods=["POST"])
@login_required
def subtask_create():
    _: Task = database.get(Task, int(request.form["id_"]))

    database.create(Task(name=request.form["name"],
                         folder=_.folder,
                         date_created=datetime.datetime.now(),
                         parent_task=_.id,
                         user=current_user.id))

    return redirect(request.referrer)


@current_app.route("/task_edit", methods=["POST"])
@login_required
def task_edit():
    _: Task = database.get(Task, int(request.form["id_"]))

    _.name = request.form["name"]
    _.note = request.form["note"]
    _.folder = int(request.form["folder"])
    _.reminder = request.form.get("reminder") is not None
    _.date_due = request.form["date_due"] if _.reminder else None

    database.update()

    return redirect(request.referrer)


@current_app.route("/task_delete")
@login_required
def task_delete():
    _: Task = database.get(Task, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)


@current_app.route("/task_toggle")
@login_required
def task_toggle():
    _: Task = database.get(Task, request.args.get("id_"))
    _.done = not _.done

    database.update()

    return redirect(request.referrer)
