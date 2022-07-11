import datetime
import random

from flask import request, render_template, current_app, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from toDo import login_manager, db
from toDo.models import User, Task, List


@login_manager.user_loader
def load_user(id_) -> User:
    _: User = User.query.get(id_)
    return _


@current_app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@current_app.route("/list")
def list():
    list_ = List.query.get(int(request.args.get("id_")))
    return render_template("list.html", list_=list_)


@current_app.route("/")
def index():
    return render_template("index.html")


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
    user_ = User(
        username=request.form["username"],
        password=generate_password_hash(request.form["password"]),
    )

    db.session.add(user_)
    db.session.commit()
    login_user(user_)

    return redirect(url_for("index"))


@current_app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    old_password = request.form["old_password"]
    new_password1 = request.form["new_password1"]
    new_password2 = request.form["new_password2"]

    if (
        check_password_hash(current_user.password, old_password)
        and new_password1 == new_password2
    ):
        current_user.password = generate_password_hash(request.form["new_password1"])
        db.session.commit()
        return redirect(request.referrer)
    else:
        return "Try again"


@current_app.route("/user_edit", methods=["POST"])
@login_required
def user_edit():
    current_user.username = request.form["username"]
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/create_task", methods=["POST"])
@login_required
def create_task():
    task_ = Task(
        description=request.form["description"],
        user=current_user.id,
        list_id=request.form["list_id"],
        date_created=datetime.datetime.now(),
    )
    db.session.add(task_)
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/edit_task", methods=["POST"])
@login_required
def edit_task():
    task_: Task = Task.query.get(int(request.form["id_"]))
    task_.description = request.form["description"]
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/delete_task")
@login_required
def delete_task():
    task_: Task = Task.query.get(int(request.args.get("id_")))
    db.session.delete(task_)
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/toggle_task")
@login_required
def toggle_task():
    task_: Task = Task.query.get(int(request.args.get("id_")))
    task_.done = not task_.done
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/create_list", methods=["POST"])
@login_required
def create_list():
    list_ = List(
        name=request.form["name"],
        color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
        user=current_user.id,
    )
    db.session.add(list_)
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/edit_list", methods=["POST"])
@login_required
def edit_list():
    list_: List = List.query.get(int(request.form["id_"]))
    list_.name = request.form["name"]
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/delete_list")
@login_required
def delete_list():
    list_: List = List.query.get(int(request.args.get("id_")))
    for i in list_.tasks:
        db.session.delete(i)
    db.session.delete(list_)
    db.session.commit()

    return redirect(url_for("index"))
