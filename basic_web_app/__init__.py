from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.FlaskSettings")

db = SQLAlchemy(app)


def register_blueprints():
    from basic_web_app.views.home_views import blueprint as home
    from basic_web_app.views.loadtest_views import blueprint as loadtest
    from basic_web_app.views.health_views import blueprint as health
    from basic_web_app.views.jobs_views import blueprint as jobs

    app.register_blueprint(home)
    app.register_blueprint(loadtest)
    app.register_blueprint(health)
    app.register_blueprint(jobs)


register_blueprints()

# Create tables from models used within blueprints
db.create_all()
