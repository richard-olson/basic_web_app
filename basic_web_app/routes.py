from flask import (
    render_template,
    current_app as app
)
import random
import logging
import datetime
import config
import math
from . import workers


cfg = config.Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    logger.debug('Attempting to get instance information')
    instances = workers.get_instance_data(
        cfg.region_name,
        cfg.tags['aws:cloudformation:stack-name']
    )

    logger.debug(f'Instance information is:')
    for idx, item in enumerate(instances):
        logger.debug(f'{idx}:{instances[idx].items()}')

    # Get RDS cluster based on database endpoint (minus aws region uri)
    logger.debug('Attempting to get rds information')
    database = workers.rds_instances(
        cfg.region_name,
        cfg.db_endpoint.split('.')[0]
    )

    # Get CloudWatch Data
    logger.debug('Attempting to get cloudwatch information')
    cloudwatch_cpu_data = workers.get_cloudwatch_data(
        cfg.region_name,
        cfg.tags['aws:autoscaling:groupName']
    )
    logger.debug('Cloudwatch response:')
    logger.debug(cloudwatch_cpu_data)

    logger.debug('Attempting to get render index.html')
    return render_template(
        'index.html',
        db_id=db_id,
        instances=instances,
        database=database,
        cfg=cfg,
        cloudwatch_cpu_data=cloudwatch_cpu_data
    )


@app.route('/load-test')
def load_test():

    load_cycles = 100000

    logger.info('Starting load-test function')
    start_time = datetime.datetime.now()
    number = 0
    for i in range(0, load_cycles):
        load = math.sqrt(random.randrange(1, 1000))
        number += load
    return str(number)
