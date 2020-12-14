import MySQLdb


class TaskModel:
    def __init__(self, descrip, priority="mid", date_added="2020-12-13", done=False, task_id=None):
        self.descrip = descrip
        self.priority = priority
        self.date_added = date_added
        self.done = done
        self.task_id = task_id

    def to_string(self):
        print(self.task_id,
              self.descrip,
              self.priority,
              self.date_added,
              bool(self.done))


class TaskCtrla:
    def __init__(self):
        pass

    def db_read(self, stmt):
        db = MySQLdb.connect()
        return

    def db_write(self, stmt):
        db = MySQLdb.connect()
        pass

    def get_task_by_id(self, task_id):
        stmt = "SELECT FROM tasks WHERE task_id = %d" % task_id
        self.db_read(stmt)
        return

    def get_all_tasks(self):
        stmt = "SELECT * FROM tasks"
        self.db_read(stmt)
        return

    def add_task(self, new_task):
        stmt = "INSERT INTO tasks(descrip, priority, date_added, done) VALUES(%s, %s, %s, %s)" % (new_task.descrip, new_task.priority, new_task.date_added, new_task.done)
        self.db_write(stmt)
        print("Added.")

    def delete_task(self, task_id):
        stmt = "DELETE FROM tasks WHERE = %d" % task_id
        self.db_write(stmt)
        print("Deleted.")

    def delete_all_tasks(self):
        stmt = "TRUNCATE TABLE tasks"
        self.db_write(stmt)
        print("All deleted.")


if __name__ == "__main__":
    pass
