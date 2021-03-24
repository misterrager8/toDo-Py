from datetime import date, datetime

from sqlalchemy import Column, Text, Date, Boolean, Integer

from modules import db


class Task(db.Model):
    __tablename__ = "tasks"

    title = Column(Text)
    notes = Column(Text)
    date_added = Column(Date)
    priority = Column(Text)
    done = Column(Boolean)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 notes: str = "",
                 date_added: date = datetime.now().date(),
                 priority: str = "Low",
                 done: bool = False):
        self.title = title.capitalize()
        self.notes = notes.capitalize()
        self.date_added = date_added
        self.priority = priority.capitalize()
        self.done = done

    def create(self):
        db.session.add(self)
        db.session.commit()

    def toggle_done(self, done: bool):
        self.done = done
        db.session.commit()

    def get_done(self):
        if self.done:
            return ["Done", "badge badge-success"]
        else:
            return ["Not Done", "badge badge-secondary"]

    def get_priority(self):
        if self.priority == "Low":
            return ["Low", "badge badge-primary"]
        elif self.priority == "Medium":
            return ["Medium", "badge badge-warning"]
        elif self.priority == "High":
            return ["High", "badge badge-danger"]

    def set_note(self, note: str):
        self.notes = note.capitalize()
        db.session.commit()

    def set_priority(self, priority: str):
        self.priority = priority.capitalize()
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


db.create_all()
