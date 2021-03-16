from flask import Flask, render_template

from modules.ctrla import TaskDB

app = Flask(__name__)

b = TaskDB().get_all()


@app.route("/")
def index():
    return render_template("index.html", task=b)


if __name__ == "__main__":
    app.run(debug=True)
