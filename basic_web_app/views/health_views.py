from flask import Blueprint

blueprint = Blueprint("health", __name__, template_folder="templates")

@blueprint.route("/health")
def health():
    return "healthy"
