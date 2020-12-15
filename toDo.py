import MySQLdb


class TaskModel:
    def __init__(self, descrip: str, priority: str = "mid", date_added: str = "2020-12-13", done: bool = False,
                 task_id: int = None):
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


class TaskDB:
    def __init__(self):
        MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB").cursor().execute(
            "CREATE TABLE IF NOT EXISTS tasks(descrip TEXT, priority TEXT, date_added TEXT, done BOOLEAN, task_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY)")

    @staticmethod
    def db_read(stmt: str) -> list:
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()
        try:
            cursor.execute(stmt)
            return cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)

    @staticmethod
    def db_write(stmt: str):
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()
        try:
            cursor.execute(stmt)
            db.commit()
        except MySQLdb.Error as e:
            print(e)

    def get_task_by_id(self, task_id: int) -> TaskModel:
        stmt = "SELECT FROM tasks WHERE task_id = %d" % task_id
        self.db_read(stmt)
        return TaskModel("")

    def get_all_tasks(self) -> list:
        stmt = "SELECT * FROM tasks"
        self.db_read(stmt)
        return []

    def add_task(self, new_task: TaskModel):
        stmt = "INSERT INTO tasks(descrip, priority, date_added, done) VALUES(%s, %s, %s, %d)" % (
            new_task.descrip, new_task.priority, new_task.date_added, new_task.done)
        self.db_write(stmt)
        print("Added.")

    def delete_task(self, task_id: int):
        stmt = "DELETE FROM tasks WHERE = %d" % task_id
        self.db_write(stmt)
        print("Deleted.")

    def delete_all_tasks(self):
        stmt = "TRUNCATE TABLE tasks"
        self.db_write(stmt)
        print("All deleted.")


if __name__ == "__main__":
    tc = TaskDB()
    tm = TaskModel("exampletask")
    tc.add_task(tm)
