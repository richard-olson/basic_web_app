from flask import Blueprint, make_response
import basic_web_app.services.loadtest_service as loadtest_service

blueprint = Blueprint("loadtest", __name__, template_folder="templates")
# no_cache = "max-age=0, no-store"


@blueprint.route("/load-test")
def load_test():
    response = make_response(loadtest_service.get_load_test())
    # response.headers["Cache-Control"] = no_cache
    return response
