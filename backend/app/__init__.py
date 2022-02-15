import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    CORS(
        app,
        resources={
            r"/*": {"origins": [r"http://localhost:*", r"http://192.168.0.11:*"]}
        },
    )
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG") or "default"

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # call init_app to complete initialization
    db.init_app(app)
    migrate.init_app(app, db)

    # create app blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .meal_delivery_task import meal_delivery_task as meal_delivery_task_blueprint

    app.register_blueprint(
        meal_delivery_task_blueprint, url_prefix="/meal_delivery_task"
    )



    from .user import user as user_blueprint

    app.register_blueprint(
        user_blueprint, url_prefix="/user"
    )

    # create route like this
    # from .contact import contact as contact_blueprint
    # app.register_blueprint(contact_blueprint, url_prefix="/contact")
    return app
