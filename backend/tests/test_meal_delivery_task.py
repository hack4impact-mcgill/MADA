import json
import unittest
import uuid
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
                "date": curr_datetime.date().isoformat(),
                "time": curr_datetime.time().isoformat(),
                "is_complete": False,
                "quantity": 1,
                "type": "test",
                "volunteer_id": None,
            },
        )

    def test_update_a_meal_delivery_task(self):
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

        response = self.client.put(
            "/meal_delivery_task/{}".format(m.id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            "/meal_delivery_task/{}".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 404)

        update_datetime = datetime.now()
        update_obj = {
            "address": "new address",
            "date": update_datetime.date().isoformat(),
            "time": update_datetime.time().isoformat(),
            "is_complete": True,
            "quantity": 2,
            "type": "update_type",
        }

        response = self.client.put(
            "/meal_delivery_task/{}".format(m.id),
            content_type="application/json",
            data=json.dumps(update_obj, default=str),
        )
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(update_obj, json_response)

    def test_delete_a_meal_delivery_task(self):
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

        response = self.client.delete("/meal_delivery_task/{}".format(m.id))
        self.assertEqual(response.status_code, 200)

        response = self.client.delete("/meal_delivery_task/{}".format(m.id))
        self.assertEqual(response.status_code, 404)
