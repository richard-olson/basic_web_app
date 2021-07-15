from app import db
import boto3


def get_db_id():
    query = "SHOW VARIABLES WHERE Variable_name = 'aurora_server_id'"
    return db.session.execute(query).fetchall()


def ec2_instances(region, stack_name):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[
        {
            'Name': 'tag:aws:cloudformation:stack-name',
            'Values': [stack_name]
        }
    ])
    return response
