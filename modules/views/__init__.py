from datetime import date

from flask import request, render_template, current_app
from werkzeug.utils import redirect

from modules import db
from modules.ctrla import Calendar, Database
from modules.model import Folder, Day, Habit, Session

database = Database()


@current_app.context_processor
def inject_all():
    all_folders = database.search(Folder, order_by="date_created desc")
    total_undone: int = sum([i.get_undone_count() for i in all_folders])
    return dict(all_folders=all_folders, total_undone=total_undone)


@current_app.route("/")
def index():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("index.html", folders_=database.search(Folder, order_by=order_by), order_by=order_by)


@current_app.route("/calendar")
def calendar():
    calendar_view = request.args.get("calendar_view", default="week")
    _ = Calendar().format_month() if calendar_view == "month" else Calendar().format_week()
    return render_template("calendar.html", cal=_, calendar_view=calendar_view)


@current_app.route("/day")
def day():
    day_date = request.args.get("day_date")
    return render_template("day.html",
                           day_date=day_date,
                           items=db.session.query(Day).filter(Day.date == day_date),
                           habits=db.session.query(Habit).all())


@current_app.route("/sessions")
def sessions():
    return render_template("sessions.html", sessions_=database.search(Session))


@current_app.route("/session_create", methods=["POST"])
def session_create():
    start_time = int(request.form["start_time"])
    stop_time = int(request.form["stop_time"])

    millis = stop_time - start_time
    mins = round((millis / (1000 * 60)) % 60, 1)

    database.create(Session(date=date.today(), length=mins))

    return redirect(request.referrer)


@current_app.route("/session_delete")
def session_delete():
    _: Session = database.get(Session, request.args.get("id_"))
    database.delete(_)

    return redirect(request.referrer)
