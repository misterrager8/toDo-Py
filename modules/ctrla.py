import os

from modules import db
from modules.model import Task


class TaskDB:
    def __init__(self):
        pass

    @staticmethod
    def create_many(stuff: list):
        for i in stuff: i.create()

    @staticmethod
    def get_all():
        return db.session.query(Task).all()

    @staticmethod
    def find_by_priority(priority: str):
        return db.session.query(Task).filter(Task.priority == priority)

    @staticmethod
    def find_by_done(done: bool):
        return db.session.query(Task).filter(Task.done == done)

    @staticmethod
    def find_by_id(id_: int):
        return db.session.query(Task).get(id_)

    @staticmethod
    def delete_all():
        db.session.execute("TRUNCATE TABLE tasks")
        db.session.commit()

    def export_all(self):
        path = os.path.join(os.path.dirname(__file__), "../output.txt")
        with open(path, "w") as f:
            for i in self.get_all(): f.write(str(i) + "\n")
