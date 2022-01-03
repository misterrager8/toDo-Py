import datetime

from flask import request, render_template, current_app, url_for
from flask_login import login_user, logout_user, current_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from modules import login_manager, db
from modules.ctrla import Database
from modules.models import User, Bullet

database = Database()


@login_manager.user_loader
def load_user(id_) -> User:
    _: User = database.get(User, id_)
    return _


@current_app.route("/profile")
def profile():
    return render_template("profile.html")


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    bullets_ = current_user.bullets.order_by(text(order_by)) if current_user.is_authenticated else None
    return render_template("index.html", order_by=order_by, bullets_=bullets_)


@current_app.route("/notes")
def notes():
    _ = current_user.bullets.filter(Bullet.type_ == "Note").order_by(text("date_created desc"))
    return render_template("notes.html", objects=_)


@current_app.route("/events")
def events():
    _ = current_user.bullets.filter(Bullet.type_ == "Event").order_by(text("date_created desc"))
    return render_template("events.html", objects=_)


@current_app.route("/tasks")
def tasks():
    _ = current_user.bullets.filter(Bullet.type_ == "Task").order_by(text("date_created desc"))
    return render_template("tasks.html", objects=_)


@current_app.route("/pinned")
def pinned():
    _ = current_user.bullets.filter(Bullet.pinned == True).order_by(text("date_created desc"))
    return render_template("pinned.html", objects=_)


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


@current_app.route("/user_edit", methods=["POST"])
def user_edit():
    current_user.first_name = request.form["first_name"]
    current_user.last_name = request.form["last_name"]
    current_user.email = request.form["email"]

    database.update()

    return redirect(request.referrer)


@current_app.route("/bullet_create", methods=["POST"])
def bullet_create():
    database.create(Bullet(type_=request.form["type_"],
                           content=request.form["content"],
                           date_created=datetime.datetime.now(),
                           user=current_user.id))

    return redirect(url_for("index"))


@current_app.route("/editor", methods=["POST", "GET"])
def editor():
    if request.method == "POST":
        _: Bullet = database.get(Bullet, int(request.form["id_"]))
        _.content = request.form["content"]

        database.update()

        return redirect(request.referrer)

    elif request.method == "GET":
        _: Bullet = database.get(Bullet, request.args.get("id_"))

        return render_template("editor.html", bullet_=_)


@current_app.route("/bullet_delete")
def bullet_delete():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    database.delete(_)

    return redirect(url_for("index"))


@current_app.route("/task_toggle")
def task_toggle():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    _.done = not _.done

    _.date_done = datetime.datetime.now() if _.done else None

    database.update()

    return redirect(url_for("index"))


@current_app.route("/pin_toggle")
def pin_toggle():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    _.pinned = not _.pinned

    database.update()

    return redirect(url_for("index"))
