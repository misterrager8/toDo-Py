import csv
import os
from datetime import datetime
from time import strptime, mktime

from modules import db
from modules.model import Task


class TaskDB:
    def __init__(self):
        pass

    @staticmethod
    def create_many(stuff: list):
        for i in stuff: i.create()

    @staticmethod
    def get_all(criterion=None):
        return db.session.query(Task).order_by(criterion)

    @staticmethod
    def find_by_priority(priority: str):
        return db.session.query(Task).filter(Task.priority == priority)

    @staticmethod
    def find_by_done(done: bool):
        return db.session.query(Task).filter(Task.done == done)

    @staticmethod
    def find_by_id(id_: int):
        return db.session.query(Task).get(id_)

    def delete(self, id_: int):
        _: Task = self.find_by_id(id_)
        db.session.delete(_)
        db.session.commit()

    @staticmethod
    def delete_all():
        db.session.execute("TRUNCATE TABLE tasks")
        db.session.commit()

    def export_all(self):
        path = os.path.join(os.path.dirname(__file__), "../output.csv")
        with open(path, "w") as f:
            w = csv.writer(f)
            for i in self.get_all():
                w.writerow([i.title,
                            i.notes,
                            i.date_added,
                            i.priority,
                            i.done])

    @staticmethod
    def import_all():
        path = os.path.join(os.path.dirname(__file__), "../input.csv")
        csv_data = csv.reader(open(path))
        for row in csv_data:
            _ = Task(row[0],
                     row[1],
                     datetime.fromtimestamp(mktime(strptime(row[2], "%Y-%m-%d"))),
                     int(row[3]),
                     bool(row[4]))
            _.create()
