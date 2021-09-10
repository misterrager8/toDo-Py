from datetime import date

from flask import request, render_template
from sqlalchemy import text

from modules import db, app
from modules.model import Folder, Habit, HabitCalendar


@app.context_processor
def inject_all():
    all_folders = db.session.query(Folder).order_by(text("date_created desc")).all()
    return dict(all_folders=all_folders)


@app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("index.html", folders_=db.session.query(Folder).order_by(text(order_by)).all(),
                           order_by=order_by)


@app.route("/calendar")
def calendar():
    current_date = date.today()
    return render_template("calendar.html",
                           habits_=db.session.query(Habit).all(),
                           month=HabitCalendar().formatmonth(current_date.year, current_date.month))
