from flask_login import UserMixin
from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey, DateTime, Date, text
from sqlalchemy.orm import relationship

from modules import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    date_joined = Column(DateTime)
    tasks = relationship("Task", lazy="dynamic")
    events = relationship("Event", lazy="dynamic")
    notes = relationship("Note", lazy="dynamic")
    habits = relationship("Habit", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_tasks(self, order_by: str = "date_created desc", filter_: str = "done is False"):
        return self.tasks.filter(Task.parent_task == None, text(filter_)).order_by(text(order_by))

    def get_events(self, order_by: str = "event_date", filter_: str = ""):
        return self.events.filter(text(filter_)).order_by(text(order_by))

    def get_notes(self, order_by: str = "date_modified desc", filter_: str = ""):
        return self.notes.filter(text(filter_)).order_by(text(order_by))


class Note(db.Model):
    __tablename__ = "notes"

    content = Column(Text)
    date_created = Column(DateTime)
    pinned = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    date_modified = Column(DateTime)

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)


class Event(db.Model):
    __tablename__ = "events"

    content = Column(Text)
    date_created = Column(DateTime)
    pinned = Column(Boolean, default=False)
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    event_date = Column(DateTime)

    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)


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
    steps = relationship("Task", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_steps(self):
        return self.steps.order_by(Task.done, text("date_created desc"))

    def get_subtasks_count(self):
        return self.steps.filter(Task.done == False).count()

    def get_subtasks_progress(self):
        done = self.steps.filter(Task.done == True).count()
        total = self.steps.count()
        perc = (done / total) * 100
        return perc


class Habit(db.Model):
    __tablename__ = "habits"

    description = Column(Text)
    color = Column(Text)
    entries = relationship("Entry", backref="habits", lazy="dynamic")
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Habit, self).__init__(**kwargs)


class Entry(db.Model):
    __tablename__ = "entries"

    datestamp = Column(Date)
    habit = Column(Integer, ForeignKey("habits.id"))
    user = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
