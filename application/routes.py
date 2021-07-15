from flask import (
    request,
    render_template,
    make_response,
    current_app as app
)
import application.workers as workers
import config

cfg = config.Config


@app.route("/")
def index():
    try:
        db_id = workers.get_db_id()
    except Exception as e:
        db_id = 'ERROR'
    ec2_instances = workers.ec2_instances(cfg.region_name, cfg.tags['aws:cloudformation:stack-name'])
    return render_template(
        'index.html',
        db_id=db_id,
        instances=ec2_instances,
        cfg=cfg
    )
