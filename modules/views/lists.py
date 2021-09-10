import datetime
import random

from flask import render_template, url_for, request, Blueprint
from sqlalchemy import text
from werkzeug.utils import redirect

from modules import db
from modules.model import List

lists = Blueprint("lists", __name__)


@lists.route("/lists")
def lists_():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("lists.html", lists_=db.session.query(List).order_by(text(order_by)).all(),
                           order_by=order_by)


@lists.route("/list_create", methods=["POST"])
def list_create():
    db.session.add(List(name=request.form["name"].title(),
                        contents=request.form["contents"].title(),
                        date_created=datetime.datetime.now(),
                        date_updated=datetime.datetime.now(),
                        color="#{:06x}".format(random.randint(0, 0xFFFFFF))))
    db.session.commit()

    return redirect(request.referrer)


@lists.route("/list_update", methods=["POST"])
def list_update():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    _.name = request.form["name"]
    _.contents = request.form["contents"]
    _.date_updated = datetime.datetime.now()
    db.session.commit()

    return redirect(request.referrer)


@lists.route("/list_delete")
def list_delete():
    id_: int = request.args.get("id_")
    _: List = db.session.query(List).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("lists"))


@lists.route("/list_clear")
def list_clear():
    db.session.execute("TRUNCATE TABLE lists")
    db.session.commit()

    return redirect(url_for("lists"))
