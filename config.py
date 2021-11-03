from os import getenv
from basic_web_app.infrastructure import instance


# Flask App Config
class FlaskSettings:

    # Load object which contains information on the AWS 
    # instance which is running Flask
    application = instance.Data()

    SECRET_KEY = application.get_secret("flask_secret")
    FLASK_APP = getenv("FLASK_APP", "app.py")
    FLASK_ENV = getenv("FLASK_ENV", "development")

    SQLALCHEMY_DATABASE_URI = application.get_database_uri()
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
