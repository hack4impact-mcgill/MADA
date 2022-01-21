from flask import Blueprint

user = Blueprint("task", __name__)

from . import routes
