import flask
from flask import Blueprint, redirect

from basic_web_app.infrastructure.view_modifiers import response
from basic_web_app.viewmodels.jobs.jobs_viewmodel import JobsIndexViewModel, JobsViewModel
from basic_web_app.viewmodels.jobs.add_job_viewmodel import AddJobViewModel
from basic_web_app.viewmodels.jobs.random_job_viewmodel import RandomJobViewModel
import basic_web_app.services.jobs_service as job_service


blueprint = Blueprint("jobs", __name__, template_folder="templates")


@blueprint.get("/jobs")
@response(template_file="jobs.html", no_caching=True)
def jobs_get():
    vm = JobsIndexViewModel()
    return vm.to_dict()


@blueprint.get("/jobs/show")
@response(template_file="partials/show_jobs.html", no_caching=True)
def jobs_show_get():
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

    else:
        response = redirect("/jobs")
        response.headers = {"hx-redirect": "/jobs"}
        return response


@blueprint.get("/jobs/cancel_add")
@response(template_file="partials/cancel_add_job.html")
def jobs_cancel_add():
    vm = AddJobViewModel()
    return vm.to_dict()


@blueprint.post("/jobs/add_random")
def jobs_add_random():

    vm = RandomJobViewModel()
    job = job_service.create_job(vm.name, vm.employer, vm.salary, vm.description)

    if not job:
        vm.error = "The job could not be created"
        return vm.to_dict()

    else:
        response = redirect("/jobs")
        response.headers = {"hx-redirect": "/jobs"}
        return response


@blueprint.delete("/jobs/delete/<job_id>")
def jobs_delete(job_id: str):

    results = job_service.delete_job(job_id)

    return ""


@blueprint.delete("/jobs/delete_all")
def jobs_delete_all():

    results = job_service.delete_all_jobs()

    resp = flask.make_response("")
    resp.headers = {"hx-redirect": "/jobs"}
    return resp
