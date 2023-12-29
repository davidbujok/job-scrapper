from flask import Blueprint, jsonify
from app.models.job import Job
from app.models.website import Website

jobs_bp = Blueprint("jobs", __name__)

# Retrieve all jobs
@jobs_bp.route("/jobs", methods=['GET'])
def get_jobs():
    all_jobs = Job.query.all()  # Assuming you're using an ORM like SQLAlchemy
    jobs_data = [job.to_dict() for job in all_jobs]  # Assuming a 'to_dict' method to serialize objects
    return jsonify(jobs_data), 200

# Retrieve jobs by website
@jobs_bp.route("/jobs/website/<string:website_name>", methods=['GET'])
def get_jobs_by_website(website_name):
    website = Website.query.filter_by(name=website_name).first()
    if website:
        jobs_data = [job.to_dict() for job in website.jobs]  # Assuming a 'jobs' relationship on 'Website' model
        return jsonify(jobs_data), 200
    else:
        return jsonify({"error": "Website not found"}), 404

# Note: Ensure that your Job and Website models have the appropriate methods and relationships set up to use the code above.
