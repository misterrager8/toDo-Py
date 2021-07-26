from datetime import date

from sqlalchemy import Column, Text, Date, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from modules import db


class Task(db.Model):
    __tablename__ = "tasks"

    name = Column(Text)
    priority = Column(Integer, default=3)
    note = Column(Text)
    done = Column(Boolean, default=False)
    date_created = Column(Date, default=date.today())
    date_due = Column(Date)
    date_done = Column(Date)
    reminder = Column(Boolean, default=False)
    folder = Column(Integer, ForeignKey("folders.id"))
    parent_task = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_priority(self):
        if self.priority == 3:
            return ["Low", "yellow"]
        elif self.priority == 2:
            return ["Medium", "orange"]
        elif self.priority == 1:
            return ["High", "red"]

    def __str__(self):
        return "%s" % self.name


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(Date, default=date.today())
    tasks = relationship("Task", backref="folders")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.name


class Habit(db.Model):
    __tablename__ = "habits"

    name = Column(Text)
    start_date = Column(Date, default=date.today())
    frequency = Column(Text, default="daily")
    end_date = Column(Date)
    reminder = Column(Boolean, default=False)
    color = Column(Text)
    days = relationship("Day")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Habit, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.name


class List(db.Model):
    __tablename__ = "lists"

    name = Column(Text)
    contents = Column(Text)
    date_created = Column(Date, default=date.today())
    date_updated = Column(Date)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.name


class Day(db.Model):
    __tablename__ = "days"

    habit = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=date.today())
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Day, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.habit, self.date)


db.create_all()
