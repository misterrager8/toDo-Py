import datetime
import random

from flask import request, render_template, current_app, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from modules import login_manager, db
from modules.ctrla import Database, HabitCalendar
from modules.models import User, Bullet, Habit, Entry

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


@current_app.route("/notes")
@login_required
def notes():
    return render_template("notes.html")


@current_app.route("/events")
@login_required
def events():
    return render_template("events.html")


@current_app.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html")


@current_app.route("/habits")
@login_required
def habits():
    today = datetime.datetime.now()
    return render_template("habits.html", cal=HabitCalendar().formatmonth(today.year, today.month))


@current_app.route("/pinned")
@login_required
def pinned():
    return render_template("pinned.html")


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
@login_required
def user_edit():
    current_user.first_name = request.form["first_name"]
    current_user.last_name = request.form["last_name"]
    current_user.email = request.form["email"]

    database.update()

    return redirect(request.referrer)


@current_app.route("/bullet_create", methods=["POST"])
@login_required
def bullet_create():
    type_ = request.form["type_"]
    content = request.form["content"]
    event_date = datetime.datetime.strptime(request.form["event_date"], "%Y-%m-%d").date() if type_ == "Event" else None
    done = False if type_ == "Task" else None

    database.create(Bullet(type_=type_,
                           content=content,
                           event_date=event_date,
                           date_created=datetime.datetime.now(),
                           done=done,
                           user=current_user.id))

    return redirect(url_for("index"))


@current_app.route("/editor", methods=["POST", "GET"])
@login_required
def editor():
    if request.method == "POST":
        _: Bullet = database.get(Bullet, int(request.form["id_"]))
        _.content = request.form["content"]
        _.event_date = datetime.datetime.strptime(request.form["event_date"],
                                                  "%Y-%m-%d").date() if _.type_ == "Event" else None

        database.update()

        return redirect(request.referrer)

    elif request.method == "GET":
        _: Bullet = database.get(Bullet, request.args.get("id_"))

        return render_template("editor.html", bullet_=_)


@current_app.route("/bullet_delete")
@login_required
def bullet_delete():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    database.delete(_)

    return redirect(url_for("index"))


@current_app.route("/task_toggle")
@login_required
def task_toggle():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    _.done = not _.done

    _.date_done = datetime.datetime.now() if _.done else None

    database.update()

    return redirect(url_for("index"))


@current_app.route("/pin_toggle")
@login_required
def pin_toggle():
    _: Bullet = database.get(Bullet, int(request.args.get("id_")))
    _.pinned = not _.pinned

    database.update()

    return redirect(url_for("index"))


@current_app.route("/habit_create", methods=["POST"])
@login_required
def habit_create():
    description = request.form["description"]

    database.create(Habit(description=description,
                          color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                          user=current_user.id))

    return redirect(url_for("habits"))


@current_app.route("/habit_delete")
@login_required
def habit_delete():
    _: Habit = database.get(Habit, int(request.args.get("id_")))

    for i in _.entries: database.delete(i)
    database.delete(_)

    return redirect(url_for("habits"))


@current_app.route("/entry_create")
@login_required
def entry_create():
    _: Habit = database.get(Habit, int(request.args.get("id_")))

    database.create(Entry(datestamp=datetime.date.today(),
                          habit=_.id,
                          user=current_user.id))

    return redirect(url_for("habits"))
