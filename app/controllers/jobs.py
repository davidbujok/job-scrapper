from flask import Blueprint
from app.models import job
from app.models import website

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/")
def job():
    return "From flask"
