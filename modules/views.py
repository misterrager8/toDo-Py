import datetime

from flask import request, render_template, current_app, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from modules import login_manager, db
from modules.ctrla import Database, HabitCalendar
from modules.models import User, Task, Note, Event

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


@current_app.route("/user_edit", methods=["POST"])
@login_required
def user_edit():
    current_user.username = request.form["username"]
    database.update()

    return redirect(request.referrer)


@current_app.route("/task_create", methods=["POST"])
@login_required
def task_create():
    _ = Task(user=current_user.id,
             content=request.form["content"],
             date_created=datetime.datetime.now())
    database.create(_)
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


@current_app.route("/event_create", methods=["POST"])
@login_required
def event_create():
    _ = Event(user=current_user.id,
              content=request.form["content"],
              date_created=datetime.datetime.now(),
              event_date=request.form["event_date"])
    database.create(_)
    return redirect(request.referrer)


@current_app.route("/event_update", methods=["POST"])
@login_required
def event_update():
    _: Event = Event.query.get(request.form["id_"])
    _.content = request.form["content"]
    _.event_date = request.form["event_date"]

    database.update()
    return redirect(request.referrer)


@current_app.route("/event_delete")
@login_required
def event_delete():
    _: Event = Event.query.get(request.args.get("id_"))

    database.delete(_)
    return redirect(request.referrer)


@current_app.route("/note_create", methods=["POST"])
@login_required
def note_create():
    _ = Note(user=current_user.id,
             content=request.form["content"],
             date_created=datetime.datetime.now(),
             date_modified=datetime.datetime.now())
    database.create(_)
    return redirect(request.referrer)


@current_app.route("/note_update", methods=["POST"])
@login_required
def note_update():
    _: Note = Note.query.get(request.form["id_"])
    _.content = request.form["content"]
    _.date_modified = datetime.datetime.now()

    database.update()
    return redirect(request.referrer)


@current_app.route("/note_delete")
@login_required
def note_delete():
    _: Note = Note.query.get(request.args.get("id_"))

    database.delete(_)
    return redirect(request.referrer)


@current_app.route("/task_pin")
@login_required
def task_pin():
    _: Task = Task.query.get(request.args.get("id_"))
    _.pinned = not _.pinned

    database.update()
    return redirect(request.referrer)


@current_app.route("/event_pin")
@login_required
def event_pin():
    _: Event = Event.query.get(request.args.get("id_"))
    _.pinned = not _.pinned

    database.update()
    return redirect(request.referrer)


@current_app.route("/note_pin")
@login_required
def note_pin():
    _: Note = Note.query.get(request.args.get("id_"))
    _.pinned = not _.pinned

    database.update()
    return redirect(request.referrer)
