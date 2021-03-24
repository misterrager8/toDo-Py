from flask import render_template

from modules import app
from modules.ctrla import TaskDB

task_db = TaskDB()


@app.route("/")
def index():
    return render_template("index.html", tasks=task_db.get_all())


@app.route("/task/<id_>")
def task_pg(id_: int):
    task = task_db.find_by_id(id_)
    return render_template("task_pg.html", task=task)
