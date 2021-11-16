from flask import Blueprint, request, render_
from basic_web_app.infrastructure.view_modifiers import response
from basic_web_app.viewmodels.home.index_viewmodel import IndexViewModel
from basic_web_app.viewmodels.home.async_index_viewmodel import AsyncIndexViewModel


blueprint = Blueprint("home", __name__, template_folder="templates")

@blueprint.get("/")
@response(template_file="index.html", no_caching=True)
def index():

    vm = IndexViewModel()

    return vm.to_dict()

@blueprint.get("/async")
async def async_index():

    vm = AsyncIndexViewModel()

    return vm.to_dict()
