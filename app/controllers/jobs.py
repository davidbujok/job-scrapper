import json
import subprocess
from flask import Blueprint, jsonify
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

@jobs_bp.route("/junior_jobs/<query>", methods=['GET', 'POST'])
def get_queried_jobs(query):
    queried_jobs = Job.query_job(query)
    return json.dumps(queried_jobs, default=str)

@jobs_bp.route("/runscript")
def run_script():
    try:
        completed_process = subprocess.run(['/home/arch/repos/job-scrapper/scrapers/scrapeall.sh'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('Script executed:', completed_process.stdout)
        return jsonify({'message': 'Script executed successfully'})
    except subprocess.CalledProcessError as e:
        print('Script execution failed with non-zero exit:', e.stderr)
        return jsonify({'message': 'Error executing script', 'error': e.stderr.decode()}), 500
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        return jsonify({'message': 'Unexpected error executing script', 'error': str(e)}), 500
