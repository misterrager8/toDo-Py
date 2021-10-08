import datetime
import random
from datetime import date

from flask import render_template, request, Blueprint
from werkzeug.utils import redirect

from modules import db
from modules.ctrla import Calendar, Database
from modules.model import Habit, Day

habits = Blueprint("habits", __name__)
database = Database()


@habits.route("/habits")
def habits_():
    return render_template("habits.html", habits_=database.search(Habit), month=Calendar().format_month())


@habits.route("/habit")
def habit():
    _: Habit = database.get(Habit, request.args.get("id_"))

    days = db.session.query(Day).filter(Day.habit == _.id)

    return render_template("habit.html", habit=_, days=days)


@habits.route("/habit_create", methods=["POST"])
def habit_create():
    database.create(Habit(name=request.form["name"].title(),
                          frequency=request.form["frequency"],
                          color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                          start_date=datetime.datetime.now()))

    return redirect(request.referrer)


@habits.route("/habit_update", methods=["POST"])
def habit_update():
    _: Habit = database.get(Habit, request.args.get("id_"))

    _.name = request.form["name"]
    _.frequency = request.form["frequency"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


@habits.route("/habit_delete")
def habit_delete():
    _: Habit = database.get(Habit, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)


@habits.route("/habit_clear")
def habit_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE habits")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(request.referrer)


@habits.route("/habit_today")
def habit_today():
    _: Habit = database.get(Habit, request.args.get("id_"))

    if _.frequency == "Daily":
        database.create(Day(habit=_.id, date=date.today()))
    if _.frequency == "Weekly":
        for i in Calendar().get_last_week():
            database.create(Day(habit=_.id, date=i))
    if _.frequency == "Monthly":
        for i in Calendar().get_last_month():
            database.create(Day(habit=_.id, date=i))

    return redirect(request.referrer)


@habits.route("/day_delete")
def day_delete():
    _: Day = database.get(Day, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)


@habits.route("/calendar_clear")
def calendar_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE days")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(request.referrer)
