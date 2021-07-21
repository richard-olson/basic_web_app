from flask import (
    render_template,
    request,
    current_app as app,
    make_response
)
import random
import logging
import datetime
import config
import math
import re
from . import (
    workers,
    logger
)


cfg = config.Config


@app.route("/")
def index():

    logger.debug('Index route accessed')
    logger.debug('Attempting to query database ID')
    try:
        db_id = workers.get_db_id()
        logger.debug('Database ID is: ' + db_id[0][1])
    except Exception as e:
        db_id = 'ERROR'
        logger.debug(e)

    if db_id != 'ERROR':
        db_id = db_id[0][1]

    logger.debug('Getting instance description')
    instances = workers.get_instance_data(
        cfg.region_name,
        cfg.tags['aws:cloudformation:stack-name']
    )

    list_of_instances = []
    for i in instances:
        list_of_instances.append(i['InstanceId'])

    logger.debug('Getting instance health information')
    health = workers.get_instance_health(
        cfg.region_name,
        list_of_instances
    )

    for tag in instances[0]['Tags']:
        if tag['Key'] == 'aws:autoscaling:groupName':
            asg_name = tag['Value']

    logger.debug(f'Getting autoscale group information for group {asg_name}')
    asg = workers.get_asg_details(cfg.region_name, asg_name)

    alb_target_group = workers.get_alb_target_health(
        cfg.region_name,
        asg['TargetGroupARNs'][0])

    logger.debug(f'Instance information is:')
    for idx, item in enumerate(instances):
        logger.debug(f'{idx}:{instances[idx].items()}')

    # Get RDS cluster based on database endpoint (minus aws region uri)
    logger.debug('Getting rds information')
    database = workers.rds_instances(
        cfg.region_name,
        cfg.db_endpoint.split('.')[0]
    )

    # Get CloudWatch Data
    logger.debug('Getting cloudwatch information')
    cloudwatch_cpu_data = workers.get_cloudwatch_data(
        cfg.region_name,
        cfg.tags['aws:autoscaling:groupName']
    )

    diagnostic_arg = request.args.get('diagnostic', default='No', type=str)
    if re.search('[Yy]es|[Tt]rue', diagnostic_arg):
        diagnostic = True
        logger.info('Diagnostic mode enabled')
    else:
        diagnostic = False

    logger.debug('Attempting to get render index.html')
    response = make_response(
        render_template(
            'index.html',
            db_id=db_id,
            instances=instances,
            database=database,
            cfg=cfg,
            cloudwatch_cpu_data=cloudwatch_cpu_data,
            diagnostic=diagnostic,
            instance_health=health,
            asg=asg,
            target_group=alb_target_group
        )
    )
    response.headers['Cache-Control'] = 'max-age=0, no-store'
    return response


@app.route('/load-test')
def load_test():

    load_cycles = 100000

    logger.info('Starting load-test function')
    start_time = datetime.datetime.now()
    number = 0
    for i in range(0, load_cycles):
        load = math.sqrt(random.randrange(1, 1000))
        number += load

    response = make_response(str(number))
    response.headers['Cache-Control'] = 'max-age=0, no-store'
    return response
