from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship

from toDo import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    tasks = relationship("Task", lazy="dynamic")
    lists = relationship("List", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_tasks(self, filter_: str = "", order_by: str = "done"):
        return self.tasks.filter(text(filter_)).order_by(text(order_by))


class List(db.Model):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    name = Column(Text)
    color = Column(Text)
    tasks = relationship("Task", backref="lists", lazy="dynamic")

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def get_tasks(self, filter_: str = "", order_by: str = "done"):
        return self.tasks.filter(text(filter_)).order_by(text(order_by))


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    list_id = Column(Integer, ForeignKey("lists.id"))
    description = Column(Text)
    date_created = Column(DateTime)
    done = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
