from flask import Blueprint, request
from basic_web_app.infrastructure.view_modifiers import response
import basic_web_app.services.job_service as job_service


blueprint = Blueprint("jobs", __name__, template_folder="templates")


@blueprint.route("/jobs", methods=["GET"])
@response(template_file="jobs.html", no_caching=True)
def jobs_get():

    data = job_service.JobsPage()

    return data.get_job_page_data()


@blueprint.route("/jobs", methods=["POST"])
@response(template_file="jobs.html")
def jobs_post():

    data = job_service.JobsPage()
    
    return data.post_job_page_data(request)
