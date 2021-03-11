import os

import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text, Boolean, Integer

app = Flask(__name__)

dotenv.load_dotenv()
db_host = os.getenv("host")
db_user = os.getenv("user")
db_passwd = os.getenv("passwd")
db_name = os.getenv("db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_passwd}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"

    title: str = Column(Text)
    notes: str = Column(Text)
    priority: str = Column(Text)
    date_created: str = Column(Text)
    done: bool = Column(Boolean)
    id: int = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 notes: str = None,
                 priority: str = "low",
                 date_created: str = "03/04/2021",
                 done: bool = False):
        self.title = title
        self.notes = notes
        self.priority = priority
        self.date_created = date_created
        self.done = done

    def add(self): pass

    def remove(self): pass

    def mark_done(self): pass

    def mark_undone(self): pass

    def to_string(self):
        print([
            self.title,
            self.notes,
            self.priority,
            self.date_created,
            self.done
        ])


db.create_all()
