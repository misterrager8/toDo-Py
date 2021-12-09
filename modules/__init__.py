import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()
db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        from modules.views.habits import habits
        from modules.views.tasks import tasks
        from modules.views.folders import folders

        app.register_blueprint(folders)
        app.register_blueprint(tasks)
        app.register_blueprint(habits)

        return app
