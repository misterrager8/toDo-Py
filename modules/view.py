from flask import render_template

from modules import app
from modules.ctrla import TaskDB

task_db = TaskDB()


@app.route("/")
def index():
    return render_template("index.html", tasks=task_db.get_all())
