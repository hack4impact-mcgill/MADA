import unittest
from app import create_app, db
from app.models import MealDeliveryTask
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

    def test_meal_delivery_task_model(self):
        curr_datetime = datetime.now()
        m = MealDeliveryTask(
            address="Test",
            date=curr_datetime,
            time=curr_datetime,
            is_complete=False,
            quantity=1,
            type="test",
        )
        db.session.add(m)
        db.session.commit()
        task = MealDeliveryTask.query.filter_by(id=m.id).first()
        task = task.serialize

        self.assertNotEquals(task.pop("id"), None)
        self.assertEquals(
            task,
            {
                "address": "Test",
                "date": curr_datetime.date(),
                "time": curr_datetime.time(),
                "is_complete": False,
                "quantity": 1,
                "type": "test",
                "volunteer_id": None,
            },
        )
