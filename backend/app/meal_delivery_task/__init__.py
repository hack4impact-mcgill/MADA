from flask import Blueprint

meal_delivery_task = Blueprint("meal_delivery_task", __name__)

from . import routes
