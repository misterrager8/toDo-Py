from flask import render_template, request

from modules.ctrla import TaskDB
from modules.model import Task, app

b = TaskDB().get_all()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_title = request.form["task_title"]
        x = Task(task_title)
        x.add()

    return render_template("index.html", task=b)


if __name__ == "__main__":
    app.run(debug=True)
