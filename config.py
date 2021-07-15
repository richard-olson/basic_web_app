"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv
import application.boot as boot

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:

    # App Configuration
    instance_id = boot.get_instance_id()
    region_name = boot.get_region()
    instance_tags = boot.get_instance(instance_id, region_name)['Tags']
    tags = {tag_kv_pair['Key']: tag_kv_pair['Value'] for tag_kv_pair in instance_tags}
    db_secret_name = '/' + tags['AppName'] + '/' + tags['Environment'] + '/RDS-Secret'
    flask_secret_name = '/' + tags['AppName'] + '/' + tags['Environment'] + '/Flask-Secret'
    db_database_name = tags['AppName'] + tags['Environment'] + 'Database'
    db_endpoint_parm = '/' + tags['AppName'] + '/' + tags['Environment'] + '/RDS-Endpoint'

    # Flask Config
    SECRET_KEY = boot.get_secret(flask_secret_name, region_name)
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    db_driver = 'mysql+pymysql://'
    db_username = 'admin'
    db_password = boot.get_secret(db_secret_name, region_name)
    db_endpoint = boot.get_parm(db_endpoint_parm, region_name)
    db_name = db_database_name
    db_uri = db_driver + db_username + ':' + db_password + '@' + db_endpoint + '/' + db_name

    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
