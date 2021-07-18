from flask import (
    render_template,
    current_app as app
)
import config
from . import workers

cfg = config.Config


@app.route("/")
def index():

    app.logger.debug('Index route accessed')
    app.logger.debug('Attempting to query database ID')
    try:
        db_id = workers.get_db_id()
        app.logger.debug('Database ID is: ' + db_id[0][1])
    except Exception as e:
        db_id = 'ERROR'
        app.logger.debug(e)

    if db_id != 'ERROR':
        db_id = db_id[0][1]

    app.logger.debug('Attempting to get instance information')
    instances = workers.get_instance_data(cfg.region_name, cfg.tags['aws:cloudformation:stack-name'])
    app.logger.debug(f'Instance information is:')
    for idx, item in enumerate(instances):
        app.logger.debug(f'{idx}:{instances[idx].items()}')

    # Get RDS cluster based on database endpoint (minus aws region uri)
    app.logger.debug('Attempting to get rds information')
    database = workers.rds_instances(cfg.region_name, cfg.db_endpoint.split('.')[0])

    app.logger.debug('Attempting to get cloudwatch information')
    cloudwatch_cpu_data = workers.get_cloudwatch_data(cfg.region_name, cfg.tags['aws:autoscaling:groupName'])
    app.logger.debug('Cloudwatch response:')
    app.logger.debug(cloudwatch_cpu_data)

    app.logger.debug('Attempting to get render index.html')
    return render_template(
        'index.html',
        db_id=db_id,
        instances=instances,
        database=database,
        cfg=cfg,
        cloudwatch_cpu_data=cloudwatch_cpu_data
    )
