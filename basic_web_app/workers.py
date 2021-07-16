import boto3
from . import db


def get_db_id():
    query = "SHOW VARIABLES WHERE Variable_name = 'aurora_server_id'"
    return db.session.execute(query).fetchall()


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
    return response


def sort_ec2_response(payload, sort_by):
    # Expects cleaned payload list
    response = sorted(payload, key=lambda k: k[sort_by])
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
