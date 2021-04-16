from datetime import date, datetime

from sqlalchemy import Column, Text, Date, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from modules import db


class Task(db.Model):
    __tablename__ = "tasks"

    title = Column(Text)
    notes = Column(Text)
    date_added = Column(Date)
    priority = Column(Integer)
    done = Column(Boolean)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 notes: str = "",
                 date_added: date = datetime.now().date(),
                 priority: int = 3,
                 done: bool = False):
        self.title = title.capitalize()
        self.notes = notes.capitalize()
        self.date_added = date_added
        self.priority = priority
        self.done = done

    def toggle_done(self, done: bool):
        self.done = done
        db.session.commit()

    def get_done(self):
        if self.done:
            return ["Done", "badge badge-success"]
        else:
            return ["Not Done", "badge badge-secondary"]

    def get_priority(self):
        if self.priority == 3:
            return ["Low", "badge badge-primary"]
        elif self.priority == 2:
            return ["Medium", "badge badge-warning"]
        elif self.priority == 1:
            return ["High", "badge badge-danger"]

    def set_note(self, note: str):
        self.notes = note.capitalize()
        db.session.commit()

    def set_priority(self, priority: int):
        self.priority = priority
        db.session.commit()

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    date_created = Column(Date)
    color = Column(Text)
    tasks = relationship("Task", backref="folders")
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 name: str,
                 date_created: date = datetime.now().date(),
                 color: str = None):
        self.name = name.capitalize()
        self.date_created = date_created
        self.color = color

    def add_task(self, task: Task):
        self.tasks.append(task)
        db.session.commit()

    def __str__(self):
        return "%d\t%s" % (self.id, self.name)


db.create_all()
