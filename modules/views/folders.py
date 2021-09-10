import datetime
import random

from flask import render_template, url_for, request, Blueprint
from werkzeug.utils import redirect

from modules import db
from modules.model import Folder

folders = Blueprint("folders", __name__)


@folders.route("/folder")
def folder():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)
    return render_template("folder.html", folder=_)


@folders.route("/folder_create", methods=["POST"])
def folder_create():
    names = request.form.getlist("name")
    for idx, i in enumerate(names):
        db.session.add(Folder(name=names[idx].title(),
                              color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
                              date_created=datetime.datetime.now()))
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder_update", methods=["POST"])
def folder_update():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    _.name = request.form["name"]
    _.color = request.form["color"]
    db.session.commit()

    return redirect(request.referrer)


@folders.route("/folder_delete")
def folder_delete():
    id_: int = request.args.get("id_")
    _: Folder = db.session.query(Folder).get(id_)

    db.session.delete(_)
    db.session.commit()

    return redirect(url_for("index"))


@folders.route("/folder_clear")
def folder_clear():
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.session.execute("TRUNCATE TABLE folders")
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    db.session.commit()

    return redirect(request.referrer)
