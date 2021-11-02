from flask import Blueprint, request
from basic_web_app.infrastructure.view_modifiers import response
from basic_web_app.viewmodels.home.index_viewmodel import IndexViewModel


blueprint = Blueprint("home", __name__, template_folder="templates")

@blueprint.route("/")
@response(template_file="index.html", no_caching=True)
def index():

    vm = IndexViewModel()

    return vm.to_dict()
