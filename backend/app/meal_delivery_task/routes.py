from . import meal_delivery_task
from flask import jsonify, abort, request
from app import db
from app.models import MealDeliveryTask

# update Task by task ID
@meal_delivery_task.route("/<uuid:id>", methods=["PUT"])
def update_meal_delivery_task(id):
    data = request.get_json(force=True)
    m = MealDeliveryTask.query.filter_by(id=id).first()

    if m is None:
        abort(404, "No meal delivery task found with specified ID.")

    if not data:
        abort(400, "No fields to update")

    address = data.get("address")
    date = data.get("date")
    time = data.get("time")
    is_complete = data.get("is_complete")
    quantity = data.get("quantity")
    type = data.get("type")

    if address is not None:
        m.address = address

    if date is not None:
        m.date = date

    if time is not None:
        m.time = time

    if is_complete is not None:
        m.is_complete = is_complete

    if quantity is not None:
        m.quantity = quantity

    if type is not None:
        m.type = type

    db.session.add(m)
    db.session.commit()

    return jsonify(m.serialize)


# delete a mealDeliveryTask by id
@meal_delivery_task.route("/<uuid:id>", methods=["DELETE"])
def delete_meal_delivery_task(id):
    m = MealDeliveryTask.query.filter_by(id=id).first()
    if m is None:
        abort(404, "No meal delivery task found with specified ID.")

    db.session.delete(m)
    db.session.commit()

    return jsonify(m.serialize)
