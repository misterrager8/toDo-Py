from sqlalchemy import Column, Text, Boolean, Integer

from modules.ctrla import db


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

    def to_string(self):
        print([
            self.title,
            self.notes,
            self.priority,
            self.date_created,
            self.done
        ])


db.create_all()
