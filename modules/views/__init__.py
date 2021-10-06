from flask import request, render_template
from sqlalchemy import text

from modules import db, app
from modules.calendar import Calendar
from modules.model import Folder, Day


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
    calendar_view = request.args.get("calendar_view", default="week")
    _ = Calendar().format_month() if calendar_view == "month" else Calendar().format_week()
    return render_template("calendar.html", cal=_, calendar_view=calendar_view)


@app.route("/day")
def day():
    day_date = request.args.get("day_date")
    return render_template("day.html", day_date=day_date, items=db.session.query(Day).filter(Day.date == day_date))
