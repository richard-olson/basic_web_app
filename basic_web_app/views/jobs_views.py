from flask import Blueprint, redirect

from basic_web_app.infrastructure.view_modifiers import response
from basic_web_app.viewmodels.jobs.jobs_viewmodel import JobsViewModel
from basic_web_app.viewmodels.jobs.add_job_viewmodel import AddJobViewModel
import basic_web_app.services.jobs_service as job_service


blueprint = Blueprint("jobs", __name__, template_folder="templates")


@blueprint.get("/jobs")
@response(template_file="jobs.html", no_caching=True)
def jobs_get():
    vm = JobsViewModel()
    return vm.to_dict()
 

@blueprint.get("/jobs/add")
@response(template_file="partials/add_job.html")
def jobs_add_get():
    vm = AddJobViewModel()
    return vm.to_dict()

@blueprint.post("/jobs/add")
@response(template_file="partials/add_job.html")
def jobs_add_post():
    vm = AddJobViewModel()
    vm.form_data()
    vm.validate()

    if vm.error:
        return vm.to_dict()

    job = job_service.create_job(vm.name, vm.employer, vm.salary, vm.description)

    if not job:
        vm.error = "The job could not be created"
        return vm.to_dict()

    vm.created = True
    return vm.to_dict()

@blueprint.get("/jobs/cancel_add")
@response(template_file="partials/cancel_add_job.html")
def jobs_cancel_add():
    vm = AddJobViewModel()
    return vm.to_dict()
