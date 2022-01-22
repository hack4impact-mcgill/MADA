import unittest
from app import create_app, db
from app.models import Task
from datetime import datetime


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_volunteer_model(self):
        curr_datetime = datetime.now()
        t = Task(
            address="Somewhere on earth",
            date=curr_datetime,
            time=curr_datetime,
            is_complete=False,
        )
        db.session.add(t)
        db.session.commit()
        task = Task.query.filter_by(address="Somewhere on earth").first()
        task = task.serialize

        self.assertNotEquals(task.pop("id"), None)

        self.assertEquals(
            task,
            {
                "address": "Somewhere on earth",
                "date": curr_datetime.date(),
                "time": curr_datetime.time(),
                "volunteer_id": None,
                "is_complete": False,
            },
        )
