from flask import Blueprint, request
from basic_web_app.infrastructure.view_modifiers import response
from basic_web_app.viewmodels.home.index_viewmodel import IndexViewModel


blueprint = Blueprint("home", __name__, template_folder="templates")
# no_cache = "max-age=0, no-store"


@blueprint.route("/")
@response(template_file="index.html")
def index():

    vm = IndexViewModel()

    # response.headers["Cache-Control"] = no_cache
    return vm.to_dict()
