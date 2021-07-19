import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app
