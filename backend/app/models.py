from . import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class UserMixin(object):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    email_address = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email_address": self.email_address,
            "username": self.username,
        }


class Volunteer(UserMixin, db.Model):
    __tablename__ = "volunteers"
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship("Task", backref=db.backref("volunteer"), lazy=True)

    @property
    def serialize(self):
        user_data = super().serialize
        user_data.update({"start_date": self.start_date})
        user_data.update({"tasks": Task.serialize_list(self.tasks)})
        return user_data


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    job_title = db.Column(db.String(64), nullable=False)

    @property
    def serialize(self):
        user_data = super().serialize
        user_data.update({"job_title": self.job_title})
        return user_data


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(64), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    volunteer_id = db.Column(UUID(as_uuid=True), db.ForeignKey("volunteers.id"))

    @property
    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "date": self.date,
            "time": self.time,
            "is_complete": self.is_complete,
            "volunteer_id": self.volunteer_id,
        }

    @staticmethod
    def serialize_list(tasks):
        json_tasks = []
        for task in tasks:
            json_tasks.append(task.serialize)
        return json_tasks
