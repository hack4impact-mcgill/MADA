import unittest
import json
from app import create_app, db
from app.models import Volunteer, Admin
from datetime import datetime
import uuid


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
        v = Volunteer(
            name="volunteer",
            phone_number="123456789",
            email_address="volunteer@gmail.com",
            username="volunteer",
            start_date=datetime.now(),
        )
        db.session.add(v)
        db.session.commit()
        volunteer = Volunteer.query.filter_by(name="volunteer").first()
        volunteer_data = volunteer.serialize
        # they are autofilled, we just need to make sure that they are not NULL
        self.assertNotEquals(volunteer_data.pop("id"), None)
        self.assertNotEquals(volunteer_data.pop("start_date"), None)

        self.assertEquals(
            volunteer_data,
            {
                "name": "volunteer",
                "phone_number": "123456789",
                "email_address": "volunteer@gmail.com",
                "username": "volunteer",
                "meal_delivery_tasks": [],
            },
        )

    def test_admin_model(self):
        a = Admin(
            name="admin",
            phone_number="123456789",
            email_address="admin@gmail.com",
            username="admin",
            job_title="admin",
        )
        db.session.add(a)
        db.session.commit()
        admin = Admin.query.filter_by(name="admin").first()
        admin_data = admin.serialize
        self.assertNotEquals(admin_data.pop("id"), None)

        self.assertEquals(
            admin_data,
            {
                "name": "admin",
                "phone_number": "123456789",
                "email_address": "admin@gmail.com",
                "username": "admin",
                "job_title": "admin",
            },
        )

    def test_update_a_user(self):
        d = datetime.now().isoformat()
        id = uuid.uuid4()
        v = Volunteer(
            id=id,
            name="volunteer",
            phone_number="123456789",
            email_address="volunteer@gmail.com",
            username="volunteer",
            start_date=d,
            meal_delivery_tasks=[],
        )

        db.session.add(v)
        db.session.commit()
        # update a user
        new_fields = {
            "name": "Test2",
            "phone_number": "987654321",
            "email_address": "test@test.com",
            "username": "test1234",
            "start_date": d,
        }

        response = self.client.put(
            "/user/{}".format(id),
            content_type="application/json",
            data=json.dumps(new_fields),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(new_fields, json_response)

        # user doesnt exist
        response = self.client.put(
            "/user/{}".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(new_fields),
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_a_user(self):
        d = datetime.now().isoformat()
        id = uuid.uuid4()
        v = Volunteer(
            id=id,
            name="volunteer",
            phone_number="123456789",
            email_address="volunteer@gmail.com",
            username="volunteer",
            start_date=d,
            meal_delivery_tasks=[],
        )

        db.session.add(v)
        db.session.commit()

        response = self.client.delete("/user/{}".format(id))
        self.assertEqual(response.status_code, 200)

        response = self.client.delete("/user/{}".format(id))
        self.assertEqual(response.status_code, 404)
