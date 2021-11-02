from flask import Blueprint, make_response
from basic_web_app.infrastructure.view_modifiers import response
import basic_web_app.services.loadtest_service as loadtest_service

blueprint = Blueprint("loadtest", __name__, template_folder="templates")


@blueprint.route("/load-test")
@response(no_caching=True) 
def load_test():
    
    return loadtest_service.get_load_test()
