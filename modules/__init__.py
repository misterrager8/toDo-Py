import os

import dotenv
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
app = Flask(__name__)

dotenv.load_dotenv()
db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_passwd}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv("secret_key")

db = SQLAlchemy(app)

from modules.views.habits import habits
from modules.views.lists import lists
from modules.views.tasks import tasks
from modules.views.folders import folders

app.register_blueprint(folders)
app.register_blueprint(tasks)
app.register_blueprint(lists)
app.register_blueprint(habits)
