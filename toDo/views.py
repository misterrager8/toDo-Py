import datetime

from flask import request, render_template, current_app, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from toDo import login_manager, db
from toDo.ctrla import Database
from toDo.models import User, Task

database = Database()


@login_manager.user_loader
def load_user(id_) -> User:
    _: User = database.get(User, id_)
    return _


@current_app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@current_app.route("/")
def index():
    return render_template("index.html")


@current_app.route("/task")
def task():
    task_: Task = database.get(Task, int(request.args.get("id_")))
    return render_template("task.html", task_=task_)


@current_app.route("/pinned")
@login_required
def pinned():
    return render_template("pinned.html")


@current_app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.session.query(User).filter(User.username == username).first()

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
    database.create(User(username=request.form["username"],
                         password=generate_password_hash(request.form["password"]),
                         date_joined=datetime.datetime.now()))

    return redirect(url_for("index"))


@current_app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    old_password = request.form["old_password"]
    new_password1 = request.form["new_password1"]
    new_password2 = request.form["new_password2"]

    if check_password_hash(current_user.password, old_password) and new_password1 == new_password2:
        current_user.password = generate_password_hash(request.form["new_password1"])
        database.update()
        return redirect(request.referrer)
    else:
        return "Try again"


@current_app.route("/user_edit", methods=["POST"])
@login_required
def user_edit():
    current_user.username = request.form["username"]
    database.update()

    return redirect(request.referrer)


@current_app.route("/task_create", methods=["POST"])
@login_required
def task_create():
    x = request.form["content"].split(", ")
    database.create_multiple([Task(user=current_user.id,
                                   content=i,
                                   date_created=datetime.datetime.now()) for i in x])

    return redirect(request.referrer)


@current_app.route("/subtask_create", methods=["POST"])
@login_required
def subtask_create():
    _: Task = Task.query.get(request.form["id_"])
    x = request.form["content"].split(", ")
    database.create_multiple([Task(user=current_user.id,
                                   parent_task=_.id,
                                   content=i,
                                   date_created=datetime.datetime.now()) for i in x])

    return redirect(request.referrer)


@current_app.route("/task_update", methods=["POST"])
@login_required
def task_update():
    _: Task = Task.query.get(request.form["id_"])
    _.content = request.form["content"]
    database.update()
    return redirect(request.referrer)


@current_app.route("/task_delete")
@login_required
def task_delete():
    _: Task = Task.query.get(request.args.get("id_"))

    database.delete_mutliple(_.subtasks)
    database.delete(_)
    return redirect(request.referrer)


@current_app.route("/task_toggle")
@login_required
def task_toggle():
    _: Task = Task.query.get(request.args.get("id_"))
    _.done = not _.done
    _.date_done = datetime.datetime.now() if _.done else None

    database.update()
    return redirect(request.referrer)


@current_app.route("/task_pin")
@login_required
def task_pin():
    _: Task = Task.query.get(request.args.get("id_"))
    _.pinned = not _.pinned

    database.update()
    return redirect(request.referrer)
