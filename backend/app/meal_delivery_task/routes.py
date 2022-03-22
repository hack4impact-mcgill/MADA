from . import meal_delivery_task
from flask import Flask, jsonify, abort
from flask import request
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

# create a mealDeliveryTask 
@meal_delivery_task.route("", methods=["POST"])
def create_meal_delivery_task():
    data = request.get_json(force=True)
    id = data.get("id")
    address = data.get("address")
    date = data.get("date")
    time = data.get("time")
    is_complete = data.get("is_complete")

    # check if all fields are empty, if so it's a garbage post
    if (
        id == ""
	    and address == ""
        and date == ""
        and time == ""
        and (is_complete == False or is_complete == True)
    ):
        abort(400, "Cannot have all empty fields for a new task")

    new_meal_delivery_task = MealDeliveryTask(
	id = id,
    	address = address,
    	date = date,
    	time = time,
    	is_complete = is_complete,
    )

    db.session.add(new_meal_delivery_task)
    db.session.commit()
    return jsonify(new_meal_delivery_task.serialize)