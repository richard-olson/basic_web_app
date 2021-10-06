from re import search
from flask import request
from basic_web_app import app, db
from basic_web_app.infrastructure import aws, instance


class HomePage:
    def __init__(self, request_data):
        self.localhost = instance.Data()
        self.fetch_ec2_data()
        self.fetch_ec2_health_data()
        self.fetch_asg_data()
        self.fetch_alb_data()
        self.fetch_db_id_data()
        self.fetch_rds_data()
        self.fetch_cloudwatch_data()
        self.set_diagnostic_mode(request_data)

    def fetch_ec2_data(self):

        self.ec2_data = aws.get_instance_data(
            self.localhost.get_region(),
            self.localhost.get_tags()["aws:cloudformation:stack-name"],
        )

    def fetch_ec2_health_data(self):

        list_of_instances = [i["InstanceId"] for i in self.ec2_data]
        self.ec2_health_data = aws.get_instance_health(
            self.localhost.get_region(), list_of_instances
        )

    def fetch_asg_data(self):

        for tag in self.ec2_data[0]["Tags"]:
            if tag["Key"] == "aws:autoscaling:groupName":
                asg_name = tag["Value"]

        self.asg_data = aws.get_asg_details(self.localhost.get_region(), asg_name)

    def fetch_alb_data(self):

        self.alb_data = aws.get_alb_target_health(
            self.localhost.get_region(), self.asg_data["TargetGroupARNs"][0]
        )

    def fetch_db_id_data(self):

        query = "SHOW VARIABLES WHERE Variable_name = 'aurora_server_id'"
        try:
            self.db_id = db.session.execute(query).fetchall()[0][1]
            # Close DB connection to ensure cached data isn't returned when the DB connection severed
            db.session.close()
            engine_container = db.get_engine(app)
            engine_container.dispose()
        except Exception as e:
            self.db_id = "ERROR"

    def fetch_rds_data(self):

        self.rds_data = aws.rds_instances(
            self.localhost.get_region(),
            self.localhost.get_database_endpoint().split(".")[0],
        )

    def fetch_cloudwatch_data(self):
        self.cloudwatch_data = aws.get_cloudwatch_data(
            self.localhost.get_region(),
            self.localhost.get_tags()["aws:autoscaling:groupName"],
        )

    def set_diagnostic_mode(self, request_data: request):

        diagnostic_arg = request_data.args.get("diagnostic", default="No", type=str)

        if search("[Yy]es|[Tt]rue", diagnostic_arg):
            self.diagnostic_mode = True
        else:
            self.diagnostic_mode = False

    def get_ec2_data(self):
        return self.ec2_data

    def get_ec2_health_data(self):
        return self.ec2_health_data

    def get_asg_data(self):
        return self.asg_data

    def get_alb_data(self):
        return self.alb_data

    def get_db_id_data(self):
        return self.db_id

    def get_rds_data(self):
        return self.rds_data

    def get_cloudwatch_data(self):
        return self.cloudwatch_data

    def get_diagnostic_mode(self):
        return self.diagnostic_mode

    def get_home_page_data(self) -> dict:

        data = {
            "localhost": self.localhost,
            "ec2_data": self.get_ec2_data(),
            "ec2_health": self.get_ec2_health_data(),
            "asg": self.get_asg_data(),
            "targetgroup": self.get_alb_data(),
            "db_id": self.get_db_id_data(),
            "rds": self.get_rds_data(),
            "cloudwatch": self.get_cloudwatch_data(),
            "diagnostic": self.get_diagnostic_mode()
        }

        return data
