import datetime
import random

from flask import render_template, url_for, request, Blueprint
from werkzeug.utils import redirect

from modules import db
from modules.ctrla import Database
from modules.model import List

lists = Blueprint("lists", __name__)
database = Database()


@lists.route("/lists")
def lists_():
    order_by = request.args.get("order_by", default="date_created desc")
    return render_template("lists.html", lists_=database.search(List, order_by=order_by), order_by=order_by)


@lists.route("/list_create", methods=["POST"])
def list_create():
    database.create(List(name=request.form["name"].title(),
                         contents=request.form["contents"].title(),
                         date_created=datetime.datetime.now(),
                         date_updated=datetime.datetime.now(),
                         color="#{:06x}".format(random.randint(0, 0xFFFFFF))))

    return redirect(request.referrer)


@lists.route("/list_update", methods=["POST"])
def list_update():
    _: List = database.get(List, request.args.get("id_"))

    _.name = request.form["name"]
    _.contents = request.form["contents"]
    _.date_updated = datetime.datetime.now()
    db.session.commit()

    return redirect(request.referrer)


@lists.route("/list_delete")
def list_delete():
    _: List = database.get(List, request.args.get("id_"))
    database.delete(_)

    return redirect(url_for("lists"))


@lists.route("/list_clear")
def list_clear():
    database.execute_stmt("TRUNCATE TABLE lists")

    return redirect(url_for("lists"))
