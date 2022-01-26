import unittest
from app import create_app, db
from app.models import Task, MealDeliveryTask
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

    def test_task_model(self):
        curr_datetime = datetime.now()
        t = Task(
            address="Somewhere on earth",
            date=curr_datetime,
            time=curr_datetime,
            is_complete=False,
        )
        db.session.add(t)
        db.session.commit()
        task = Task.query.filter_by(id=t.id).first()
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
                "meal_delivery_tasks": [],
            },
        )

    def test_meal_delivery_task_model(self):
        m = MealDeliveryTask(
            quantity=1,
            type="test",
        )
        db.session.add(m)
        db.session.commit()
        task = MealDeliveryTask.query.filter_by(id=m.id).first()
        task = task.serialize

        self.assertNotEquals(task.pop("id"), None)
        self.assertEquals(task, {"quantity": 1, "type": "test", "task_id": None})

    def test_meal_with_task(self):
        m = MealDeliveryTask(
            quantity=1,
            type="test",
        )
        db.session.add(m)
        db.session.add(m)
        curr_datetime = datetime.now()
        t = Task(
            address="Somewhere on earth",
            date=curr_datetime,
            time=curr_datetime,
            is_complete=False,
            meal_delivery_tasks=[m],
        )
        db.session.add(t)
        db.session.commit()
        task = Task.query.filter_by(id=t.id).first()
        task = task.serialize

        self.assertNotEquals(task.pop("id"), None)
        self.assertNotEquals(task["meal_delivery_tasks"][0].pop("id"), None)

        self.assertEquals(
            task,
            {
                "address": "Somewhere on earth",
                "date": curr_datetime.date(),
                "time": curr_datetime.time(),
                "volunteer_id": None,
                "is_complete": False,
                "meal_delivery_tasks": [
                    {"quantity": 1, "type": "test", "task_id": t.id}
                ],
            },
        )
