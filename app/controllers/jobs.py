import json
from flask import Blueprint
from app.models.job import Job

jobs_bp = Blueprint("jobs", __name__)

# Retrieve all jobs
@jobs_bp.route("/jobs", methods=['GET'])
def get_jobs():
    jobs = Job.get_all_jobs()
    return json.dumps(jobs, default=str)

@jobs_bp.route("/junior_jobs", methods=['GET'])
def get_junior_jobs():
    junior_jobs = Job.get_junior_jobs()
    return json.dumps(junior_jobs, default=str)
