import datetime
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
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("index.html", folders_=db.session.query(Folder).order_by(text(order_by)).all(),
                           order_by=order_by)


@app.route("/folder")
def folder():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)
    return render_template("folder.html", folder=_)


@app.route("/tasks")
def tasks():
    order_by = request.args.get("order_by", default="tasks.date_created desc")
    return render_template("tasks.html",
                           tasks_=db.session.query(Task).join(Folder).order_by(Task.done, text(order_by)).all(),
                           order_by=order_by)


@app.route("/task_create", methods=["POST"])
def task_create():
    names = request.form.getlist("name")
    priorities = request.form.getlist("priority")
    folders = request.form.getlist("folder")

    for idx, i in enumerate(names):
        _ = Task(name=names[idx],
                 priority=int(priorities[idx]),
                 folder=int(folders[idx]),
                 date_created=datetime.datetime.now())
        db.session.add(_)

    db.session.commit()

    return redirect(request.referrer)


@app.route("/task_update", methods=["POST"])
def task_update():
    id_: int = request.args.get("id_")
    _: Task = db.session.query(Task).get(id_)

    _.name = request.form["name"]
    _.priority = int(request.form["priority"])
    _.note = request.form["note"]
    _.folder = int(request.form["folder"])
    db.session.commit()

    return redirect(request.referrer)


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

    if not _.done:
        _.done = True
        _.date_done = datetime.datetime.now()
    else:
        _.done = False
        _.date_done = None
    db.session.commit()

    return redirect(request.referrer)


@app.route("/task_clear")
def task_clear():
    db.session.execute("TRUNCATE TABLE tasks")
    db.session.commit()

    return redirect(request.referrer)


@app.route("/folder_create", methods=["POST"])
def folder_create():
    db.session.add(Folder(name=request.form["name"].title(),
                          color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                          date_created=datetime.datetime.now()))
    db.session.commit()

    return redirect(request.referrer)


@app.route("/folder_update", methods=["POST"])
def folder_update():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    _.name = request.form["name"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


@app.route("/folder_delete")
def folder_delete():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/folder_clear")
def folder_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE folders")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(request.referrer)


@app.route("/habits")
def habits():
    current_date = date.today()
    return render_template("habits.html",
                           habits_=db.session.query(Habit).all(),
                           month=HabitCalendar().formatmonth(current_date.year, current_date.month))


@app.route("/calendar")
def calendar():
    current_date = date.today()
    return render_template("calendar.html",
                           habits_=db.session.query(Habit).all(),
                           month=HabitCalendar().formatmonth(current_date.year, current_date.month))


@app.route("/calendar_clear")
def calendar_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE days")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(url_for("calendar"))


@app.route("/habit_create", methods=["POST"])
def habit_create():
    db.session.add(Habit(name=request.form["name"].title(),
                         frequency=request.form["frequency"],
                         color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                         start_date=datetime.datetime.now()))
    db.session.commit()

    return redirect(request.referrer)


@app.route("/habit_update", methods=["POST"])
def habit_update():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    _.name = request.form["name"]
    _.frequency = request.form["frequency"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


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

    week = [date.today() + datetime.timedelta(days=i) for i in
            range(0 - date.today().weekday(), 7 - date.today().weekday())]
    month = HabitCalendar().itermonthdates(int(date.today().year), int(date.today().month))

    if _.frequency == "Daily":
        db.session.add(Day(habit=_.id, date=date.today()))
    if _.frequency == "Weekly":
        for i in week:
            db.session.add(Day(habit=_.id, date=i))
    if _.frequency == "Monthly":
        for i in month:
            db.session.add(Day(habit=_.id, date=i))

    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/habit_clear")
def habit_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE habits")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(url_for("habits"))


@app.route("/lists")
def lists():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("lists.html", lists_=db.session.query(List).order_by(text(order_by)).all(),
                           order_by=order_by)


@app.route("/list_create", methods=["POST"])
def list_create():
    db.session.add(List(name=request.form["name"].title(),
                        contents=request.form["contents"].title(),
                        date_created=datetime.datetime.now(),
                        date_updated=datetime.datetime.now(),
                        color="#{:06x}".format(random.randint(0, 0xFFFFFF))))
    db.session.commit()

    return redirect(request.referrer)


@app.route("/list_update", methods=["POST"])
def list_update():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    _.name = request.form["name"]
    _.contents = request.form["contents"]
    _.date_updated = datetime.datetime.now()
    db.session.commit()

    return redirect(request.referrer)


@app.route("/list_delete")
def list_delete():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("lists"))


@app.route("/list_clear")
def list_clear():
    db.session.execute("TRUNCATE TABLE lists")
    db.session.commit()

    return redirect(url_for("lists"))
