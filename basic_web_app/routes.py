from flask import (
    render_template,
    current_app as app
)
import config
from . import workers

cfg = config.Config


@app.route("/")
def index():

    try:
        db_id = workers.get_db_id()
    except Exception as e:
        db_id = 'ERROR'

    instances = workers.get_instance_data(cfg.region_name, cfg.tags['aws:cloudformation:stack-name'])

    # Get RDS cluster based on database endpoint (minus aws region uri)
    database = workers.rds_instances(cfg.region_name, cfg.db_endpoint.split('.')[0])
    return render_template(
        'index.html',
        db_id=db_id[0][1],
        instances=instances,
        database=database,
        cfg=cfg
    )
