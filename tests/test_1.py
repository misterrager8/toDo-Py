import unittest

from modules.ctrla import DB
from modules.model import Task


class MyTestCase(unittest.TestCase):
    def test_create(self):
        x = DB()
        x.create(Task("Take out the trash"))
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
