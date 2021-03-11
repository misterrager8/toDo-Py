from modules.model import db, Task


class TaskDB:
    def __init__(self): pass

    @staticmethod
    def get_all():
        return db.session.query(Task).all()

    @staticmethod
    def get_all_done():
        return db.session.query(Task).filter(Task.done)

    @staticmethod
    def get_all_undone():
        return db.session.query(Task).filter(not Task.done)

    @staticmethod
    def remove_all():
        db.session.execute("TRUNCATE table tasks")
        db.session.commit()

    @staticmethod
    def mark_all_undone():
        db.session.execute("UPDATE tasks SET done = False")
        db.session.commit()

    @staticmethod
    def mark_all_done():
        db.session.execute("UPDATE tasks SET done = True")
        db.session.commit()
