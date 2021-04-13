import csv
import os

from sqlalchemy import text

from modules import db


class ToDoDB:
    def __init__(self):
        pass

    @staticmethod
    def create_one(item):
        db.session.add(item)
        db.session.commit()

    @staticmethod
    def create_many(stuff: list):
        for i in stuff:
            db.session.add(i)
            db.session.commit()

    @staticmethod
    def get_all(item_type,
                order_by: str = "",
                filter_: str = ""):
        return db.session \
            .query(item_type) \
            .order_by(text(order_by)) \
            .filter(text(filter_))

    @staticmethod
    def find_by_id(item_type,
                   id_: int):
        return db.session \
            .query(item_type) \
            .get(id_)

    @staticmethod
    def delete_one(item):
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def delete_all(table_name: str):
        db.session.execute("TRUNCATE TABLE '%s'" % table_name)
        db.session.commit()

    def export_all(self, item_type):
        path = os.path.join(os.path.dirname(__file__), "../output.csv")
        with open(path, "w") as f:
            w = csv.writer(f)
            for i in self.get_all(item_type):
                w.writerow(str(i))
