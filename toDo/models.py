from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship

from toDo import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    date_joined = Column(DateTime)
    tasks = relationship("Task", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_tasks(
        self, order_by: str = "date_created desc", filter_: str = "done is False"
    ):
        return self.tasks.filter(Task.parent_task == None, text(filter_)).order_by(
            Task.done, text(order_by)
        )


class Task(db.Model):
    __tablename__ = "tasks"

    content = Column(Text)
    date_created = Column(DateTime)
    pinned = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    done = Column(Boolean, default=False)
    date_done = Column(DateTime)
    parent_task = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_subtasks(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.subtasks.filter(text(filter_)).order_by(Task.done, text(order_by))
