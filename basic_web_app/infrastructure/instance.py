from ec2_metadata import ec2_metadata
from os import getenv
import basic_web_app.infrastructure.aws as aws


class Data:
    def __init__(self) -> None:
        self.instance_id = ec2_metadata.instance_id
        self.region = ec2_metadata.region
        self.app_name = getenv("APPNAME")
        self.env_state = getenv("APPENV").capitalize()
        self.set_tags()
        
    def get_instance_id(self):
        return self.instance_id

    def get_region(self):
        return self.region

    def _retrieve_aws_tags(self):
        instance_tags = aws.get_instance(self.instance_id, self.region)["Tags"]
        # Convert tags from [{"Key": TheKey, {"Value": TheValue}] to {TheKey: TheValue}
        aws_tags = {
            tag_kv_pair["Key"]: tag_kv_pair["Value"] for tag_kv_pair in instance_tags
        }
        return aws_tags
    
    def set_tags(self):
        self.tags = self._retrieve_aws_tags()

    def get_object_name(self, object: str):
        tags = self.get_tags()
        base_name = "/" + tags["AppName"] + "/" + tags["Environment"]
        names = {}
        names["flask_secret"] = base_name + "/Flask-Secret"
        names["db_secret"] = base_name + "/RDS-Secret"
        names["db_name"] = tags["AppName"] + tags["Environment"] + "Database"
        names["db_endpoint"] = base_name + "/RDS-Endpoint"

        return names[object]

    def get_database_endpoint(self):
        db_endpoint = aws.get_parm(self.get_object_name("db_endpoint"), self.region)
        return db_endpoint

    def get_secret(self, secret_name: str):
        # secret_name should be flask_secret or db_secret to match the object names
        self.secret = aws.get_secret(self.get_object_name(secret_name), self.region)
        return self.secret

    def get_tags(self):
        return self.tags

    def get_database_uri(self):
        # Database
        db_driver = "mysql+pymysql://"
        db_username = "admin"
        db_password = self.get_secret("db_secret")
        db_creds = db_username + ":" + db_password
        db_endpoint = self.get_database_endpoint()
        db_name = self.get_object_name("db_name")
        db_uri = db_driver + db_creds + "@" + db_endpoint + "/" + db_name

        return db_uri
