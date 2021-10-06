from flask import Blueprint, request
from basic_web_app.infrastructure.view_modifiers import response
import basic_web_app.services.home_service as home_service


blueprint = Blueprint("home", __name__, template_folder="templates")
# no_cache = "max-age=0, no-store"


@blueprint.route("/")
@response(template_file="index.html")
def index():

    data = home_service.HomePage(request)

    # response.headers["Cache-Control"] = no_cache
    return data.get_home_page_data()
