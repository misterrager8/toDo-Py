import random
from datetime import date

from flask import render_template, url_for, request
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import app, db
from modules.model import Task, Folder, Habit, List, Day, HabitCalendar


@app.context_processor
def inject_all():
    all_folders = db.session.query(Folder).order_by(text("date_created desc")).all()
    return dict(all_folders=all_folders)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks")
def tasks():
    order_by = request.args.get("order_by", default="tasks.date_created desc")
    return render_template("tasks.html", tasks_=db.session.query(Task).join(Folder).order_by(text(order_by)).all(), order_by=order_by)


@app.route("/task_create", methods=["POST"])
def task_create():
    db.session.add(Task(name=request.form["name"].title(),
                        priority=int(request.form["priority"]),
                        note=request.form["note"],
                        folder=int(request.form["folder"]),
                        date_created=date.today()))
    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/task_update", methods=["POST"])
def task_update():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    _.name = request.form["name"]
    _.priority = int(request.form["priority"])
    _.note = request.form["note"]
    _.folder = int(request.form["folder"])
    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/task_delete")
def task_delete():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/task_toggle")
def task_toggle():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    db.session.commit()

    return redirect(url_for("tasks"))


@app.route("/folders")
def folders():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("folders.html", folders_=db.session.query(Folder).order_by(text(order_by)).all(), order_by=order_by)


@app.route("/folder_create", methods=["POST"])
def folder_create():
    db.session.add(Folder(name=request.form["name"].title(),
                          color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                          date_created=date.today()))
    db.session.commit()

    return redirect(url_for("folders"))


@app.route("/folder_update", methods=["POST"])
def folder_update():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    _.name = request.form["name"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(url_for("folders"))


@app.route("/folder_delete")
def folder_delete():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("folders"))


@app.route("/habits")
def habits():
    return render_template("habits.html", habits_=db.session.query(Habit).all(),
                           month=HabitCalendar().formatmonth(date.today().year, date.today().month))


@app.route("/habit_create", methods=["POST"])
def habit_create():
    db.session.add(Habit(name=request.form["name"].title(),
                         frequency=request.form["frequency"],
                         color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                         start_date=date.today()))
    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/habit_update", methods=["POST"])
def habit_update():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    _.name = request.form["name"]
    _.frequency = request.form["frequency"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/habit_delete")
def habit_delete():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/habit_today")
def habit_today():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    db.session.add(Day(habit=_.id,
                       date=date.today()))
    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/lists")
def lists():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("lists.html", lists_=db.session.query(List).order_by(text(order_by)).all(), order_by=order_by)


@app.route("/list_create")
def list_create():
    db.session.add(List(name=request.form["name"].title(),
                        contents=request.form["contents"].title(),
                        date_created=date.today()))
    db.session.commit()

    return redirect(url_for("lists"))


@app.route("/list_update", methods=["POST"])
def list_update():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    _.name = request.form["name"]
    _.contents = request.form["contents"]
    db.session.commit()

    return redirect(url_for("lists"))


@app.route("/list_delete")
def list_delete():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("lists"))
