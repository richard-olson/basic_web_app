from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import application.boot as boot

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from application import routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app


wsgi = create_app()

if __name__ == "__main__":
    wsgi.run(host="0.0.0.0", port=5000)