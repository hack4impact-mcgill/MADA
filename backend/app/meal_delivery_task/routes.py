from . import meal_delivery_task
from flask import Flask, jsonify, abort
from app import db
from app.models import MealDeliveryTask

# delete a mealDeliveryTask by id
@meal_delivery_task.route("/<uuid:id>", methods=["DELETE"])
def delete_meal_delivery_task(id):
    m = MealDeliveryTask.query.filter_by(id=id).first()
    if m is None:
        abort(404, "No meal delivery task found with specified ID.")

    db.session.delete(m)
    db.session.commit()

    return jsonify(m.serialize)
