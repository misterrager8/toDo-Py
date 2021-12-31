from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from modules import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    date_joined = Column(DateTime)
    tasks = relationship("Task", lazy="dynamic")
    folders = relationship("Folder", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Task(db.Model):
    __tablename__ = "tasks"

    name = Column(Text)
    note = Column(Text)
    done = Column(Boolean, default=False)
    date_created = Column(DateTime)
    date_due = Column(DateTime)
    date_done = Column(DateTime)
    reminder = Column(Boolean, default=False)
    folder = Column(Integer, ForeignKey("folders.id"))
    user = Column(Integer, ForeignKey("users.id"))
    parent_task = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime)
    user = Column(Integer, ForeignKey("users.id"))
    tasks = relationship("Task", backref="folders", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def get_undone_count(self) -> int:
        return self.tasks.filter(Task.parent_task == None, Task.done == False).count()
