from re import search
from basic_web_app import app, db
from basic_web_app.infrastructure import aws, instance


def get_localhost_data():
    return instance.Data()


def get_ec2_data(region, tags):

    ec2_data = aws.get_instance_data(
        region,
        tags["aws:cloudformation:stack-name"],
    )

    return ec2_data


def get_ec2_health_data(region, ec2_data):

    list_of_instances = [i["InstanceId"] for i in ec2_data]
    ec2_health_data = aws.get_instance_health(region, list_of_instances)

    return ec2_health_data


def get_asg_data(region, ec2_data):

    for tag in ec2_data[0]["Tags"]:
        if tag["Key"] == "aws:autoscaling:groupName":
            asg_name = tag["Value"]

    asg_data = aws.get_asg_details(region, asg_name)

    return asg_data


def get_alb_data(region, asg_data):

    alb_data = aws.get_alb_target_health(region, asg_data["TargetGroupARNs"][0])

    return alb_data


def get_db_id_data():

    query = "SHOW VARIABLES WHERE Variable_name = 'aurora_server_id'"
    try:
        db_id = db.session.execute(query).fetchall()[0][1]
        # Close DB connection to ensure cached data isn't returned when the DB connection severed
        db.session.close()
        engine_container = db.get_engine(app)
        engine_container.dispose()
    except Exception as e:
        db_id = "ERROR"

    return db_id


def get_rds_data(region, endpoint):

    rds_data = aws.rds_instances(
        region,
        endpoint.split(".")[0],
    )

    return rds_data


def get_cloudwatch_data(region, tags):
    
    cloudwatch_data = aws.get_cloudwatch_data(
        region,
        tags["aws:autoscaling:groupName"],
    )

    return cloudwatch_data


def get_diagnostic_mode(request_data):

    if "diagnostic" in request_data:
        if search("[Yy]es|[Tt]rue", request_data["diagnostic"]):
            diagnostic_mode = True
    else:
        diagnostic_mode = False

    return diagnostic_mode
