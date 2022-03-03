from . import user
from flask import Flask, jsonify, abort, request
from app import db
from app.models import Admin, Volunteer

# update a user by id
@user.route("/<uuid:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json(force=True)
    u1 = Admin.query.filter_by(id=id).first()
    u2 = Volunteer.query.filter_by(id=id).first()
    if u1 is not None:
        u = u1
        job_title = data.get("job_title")
        if job_title is not None:
            u.job_title = job_title
    elif u2 is not None:
        u = u2
        start_date = data.get("start_date")
        if start_date is not None:
            u.start_date = start_date
    else:
        abort(404, "No user found with specified ID.")

    name = data.get("name")
    phone_number = data.get("phone_number")
    email_address = data.get("email_address")
    username = data.get("username")
    if name is not None:
        u.name = name
    if phone_number is not None:
        u.phone_number = phone_number
    if email_address is not None:
        u.email_address = email_address
    if username is not None:
        u.username = username
    db.session.add(u)
    db.session.commit()
    return jsonify(u.serialize)


# delete a user by id
@user.route("/<uuid:id>", methods=["DELETE"])
def delete_user(id):
    u1 = Admin.query.filter_by(id=id).first()
    u2 = Volunteer.query.filter_by(id=id).first()
    if u1 is not None:
        u = u1
    elif u2 is not None:
        u = u2
    else:
        abort(404, "No user found with specified ID.")

    db.session.delete(u)
    db.session.commit()
    return jsonify(u.serialize)
