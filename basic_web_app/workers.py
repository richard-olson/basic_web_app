import datetime
import boto3
from . import (
    logger
)
from flask import current_app as app
from .models import Jobs, db


def get_db_id():
    query = "SHOW VARIABLES WHERE Variable_name = 'aurora_server_id'"
    result = db.session.execute(query).fetchall()

    # Close DB connection to ensure cached data isn't returned
    # when the DB connection severed
    db.session.close()
    engine_container = db.get_engine(app)
    engine_container.dispose()

    return result


def get_instance_data(region, stack_name):
    data = ec2_instances(region, stack_name)
    cleaned_data = clean_ec2_response(data)
    sorted_data = sort_ec2_response(cleaned_data, 'InstanceId')
    return sorted_data


def ec2_instances(region, stack_name):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'tag:aws:cloudformation:stack-name',
            'Values': [stack_name]
        }
    ])
    return response


def clean_ec2_response(payload):
    response = []
    for r in payload['Reservations']:
        for instance in r['Instances']:
            if instance['State']['Name'] != 'terminated':
                response.append(instance)

    for r in response:
        r['Uptime'] = (
            datetime.datetime.now(datetime.timezone.utc) - r['LaunchTime'])

    return response


def sort_ec2_response(payload, sort_by):
    # Expects cleaned payload list
    response = sorted(payload, key=lambda k: k[sort_by])
    return response


def get_instance_health(region, instances):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instance_status(
        InstanceIds=instances
    )

    return response['InstanceStatuses']


def get_asg_details(region, name):
    client = boto3.client('autoscaling', region_name=region)
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            name
        ]
    )

    return response['AutoScalingGroups'][0]


def get_alb_target_health(region, name):
    client = boto3.client('elbv2', region_name=region)
    response = client.describe_target_health(
        TargetGroupArn=name
    )

    return response


def rds_instances(region, cluster_id):
    rds = boto3.client('rds', region_name=region)
    response = rds.describe_db_instances(
        Filters=[
            {
                'Name': 'db-cluster-id',
                'Values': [cluster_id]
            }
        ]
    )
    return response['DBInstances']


def get_cloudwatch_data(region, asg_name):
    cw = boto3.client('cloudwatch', region_name=region)
    response = cw.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'getASGCPUUtilization',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [
                            {
                                'Name': 'AutoScalingGroupName',
                                'Value': asg_name
                            }
                        ]
                    },
                    'Period': 10,
                    'Stat': 'Average'
                }
            }
        ],
        StartTime=datetime.datetime.now() - datetime.timedelta(minutes=120),
        EndTime=datetime.datetime.now()
    )
    logger.debug('Cloudwatch response:')
    logger.debug(response['MetricDataResults'][0])

    if len(response['MetricDataResults'][0]['Values']) > 0:
        response = response['MetricDataResults'][0]['Values'][0]
    else:
        response = 0

    return response


def create_job(name: str, employer: str, salary: int, description: str):

    job = Jobs(
        name=name,
        salary=salary.strip('$ '),
        employer=employer,
        description=description,
        created_date=datetime.datetime.now(
            tz=datetime.timezone(
                datetime.timedelta(hours=10)
            )
        )
    )

    logger.info('Creating database entry')
    logger.info(job)
    db.session.add(job)
    db.session.commit()

    result = 'Job created'

    return result
