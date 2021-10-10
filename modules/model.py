import datetime

from sqlalchemy import Column, Text, Date, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from modules import db


class Task(db.Model):
    __tablename__ = "tasks"

    name = Column(Text)
    note = Column(Text)
    done = Column(Boolean, default=False)
    date_created = Column(DateTime)
    date_due = Column(Date)
    date_done = Column(DateTime)
    reminder = Column(Boolean, default=False)
    folder = Column(Integer, ForeignKey("folders.id"))
    parent_task = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_subtasks_count(self):
        return self.subtasks.filter(Task.done == False).count()

    def get_subtasks_progress(self):
        done = self.subtasks.filter(Task.done == True).count()
        total = self.subtasks.count()
        perc = (done / total) * 100
        return perc

    def toggle_done(self):
        self.date_done = None if self.done else datetime.date.today()
        self.done = not self.done

        db.session.commit()

    def __str__(self):
        return "%s" % self.name


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime)
    tasks = relationship("Task", backref="folders", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def get_tasks(self):
        return self.tasks.order_by(Task.done, Task.date_created.desc()).filter(Task.parent_task == None)

    def get_undone_count(self) -> int:
        return self.tasks.filter(Task.parent_task == None, Task.done == False).count()

    def __str__(self):
        return "%s" % self.name


class Habit(db.Model):
    __tablename__ = "habits"

    name = Column(Text)
    start_date = Column(DateTime)
    frequency = Column(Text, default="daily")
    end_date = Column(Date)
    reminder = Column(Boolean, default=False)
    color = Column(Text)
    days = relationship("Day", backref="habits", cascade="all, delete")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Habit, self).__init__(**kwargs)

    def add_day(self, date: datetime.date):
        db.session.add(Day(habit=self.id, date=date))
        db.session.commit()

    def __str__(self):
        return "%s" % self.name


class List(db.Model):
    __tablename__ = "lists"

    name = Column(Text)
    contents = Column(Text)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    color = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def get_items(self):
        return self.contents.split("\n")

    def __str__(self):
        return "%s" % self.name


class Day(db.Model):
    __tablename__ = "days"

    habit = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Day, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.habit, self.date)


db.create_all()
