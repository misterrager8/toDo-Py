import datetime
import random
from datetime import date

from flask import render_template, url_for, request, Blueprint
from werkzeug.utils import redirect

from modules import db
from modules.model import Habit, HabitCalendar

habits = Blueprint("habits", __name__)


@habits.route("/habits")
def habits_():
    current_date = date.today()
    return render_template("habits.html",
                           habits_=db.session.query(Habit).all(),
                           month=HabitCalendar().formatmonth(current_date.year, current_date.month))


@habits.route("/habit")
def habit():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)
    return render_template("habit.html", habit=_)


@habits.route("/habit_create", methods=["POST"])
def habit_create():
    db.session.add(Habit(name=request.form["name"].title(),
                         frequency=request.form["frequency"],
                         color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                         start_date=datetime.datetime.now()))
    db.session.commit()

    return redirect(request.referrer)


@habits.route("/habit_update", methods=["POST"])
def habit_update():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    _.name = request.form["name"]
    _.frequency = request.form["frequency"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


@habits.route("/habit_delete")
def habit_delete():
    id_: int = request.args.get("id_")
    _: Habit = db.session.query(Habit).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("habits"))


@habits.route("/habit_clear")
def habit_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE habits")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(url_for("habits"))
