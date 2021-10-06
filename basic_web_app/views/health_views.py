from flask import Blueprint

blueprint = Blueprint("health", __name__, template_folder="templates")
# no_cache = "max-age=0, no-store"


@blueprint.route("/health")
def health():
    return "healthy"
