import unittest
from app import create_app, db
from app.models import Volunteer, Admin
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
                "tasks": [],
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
