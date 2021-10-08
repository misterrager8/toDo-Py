import datetime
import random

from flask import render_template, url_for, request, Blueprint
from werkzeug.utils import redirect

from modules import db
from modules.ctrla import Database
from modules.model import Folder

folders = Blueprint("folders", __name__)
database = Database()


@folders.route("/folder")
def folder():
    _: Folder = database.get(Folder, request.args.get("id_"))
    return render_template("folder.html", folder=_)


@folders.route("/folder_create", methods=["POST"])
def folder_create():
    names = request.form.getlist("name")
    for idx, i in enumerate(names):
        database.create(Folder(name=names[idx].title(),
                               color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                               date_created=datetime.datetime.now()))

    return redirect(request.referrer)


@folders.route("/folder_update", methods=["POST"])
def folder_update():
    _: Folder = database.get(Folder, request.args.get("id_"))

    _.name = request.form["name"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder_delete")
def folder_delete():
    _: Folder = database.get(Folder, request.args.get("id_"))
    database.delete(_)

    return redirect(url_for("index"))


@folders.route("/folder_clear")
def folder_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE folders")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(request.referrer)
