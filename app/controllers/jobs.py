import json
import os
import subprocess
from flask import Blueprint, jsonify
from app.models.job import Job
from app.models.user import User

jobs_bp = Blueprint("jobs", __name__)

# Retrieve all jobs
@jobs_bp.route("/jobs", methods=['GET'])
def get_jobs():
    jobs = Job.get_all_jobs()
    return json.dumps(jobs, default=str)

@jobs_bp.route("/jobs/user/<id>", methods=['GET', 'POST'])
def get_all_jobs(id):
    all_jobs = User.get_user_jobs(id)
    print(all_jobs)
    return json.dumps(all_jobs, default=str)

@jobs_bp.route("/junior_jobs", methods=['GET'])
def get_junior_jobs():
    junior_jobs = Job.get_junior_jobs()
    return json.dumps(junior_jobs, default=str)

@jobs_bp.route("/junior_jobs/<query>", methods=['GET', 'POST'])
def get_queried_jobs(query):
    queried_jobs = Job.query_job(query)
    return json.dumps(queried_jobs, default=str)

@jobs_bp.route("/hide_job/<id>", methods=['GET', 'POST'])
def hide_job(id):
    queried_jobs = Job.hide_job(id)
    return ""
    # return json.dumps(queried_jobs, default=str)

@jobs_bp.route("/runscript/<param1>/<param2>", methods=['GET', 'POST'])
def run_script(param1, param2):
    print(f"Received request with param1: {param1}, param2: {param2}")

    # Using the system's Python interpreter
    command_linkedin = ['python', '/home/arch/repos/job-scrapper/scrapers/linkedin-scrape.py', param1, param2]
    command_indeed = ['python', '/home/arch/repos/job-scrapper/scrapers/indeed-scrape.py', param1, param2]

    try:
        completed_linkedin_process = subprocess.Popen(
            command_linkedin,
            preexec_fn=os.setsid,   # Use os.setsid() to start the process in a new session (UNIX only)
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout1, stderr1 = completed_linkedin_process.communicate()
        if completed_linkedin_process.returncode == 0 or completed_linkedin_process.returncode == 1:
            print("First process completed successfully.")
            print("Output:\n", stdout1)

            try:
                completed_indeed_process = subprocess.Popen(
                    command_indeed,
                    preexec_fn=os.setsid,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

            except subprocess.CalledProcessError as e:
                print(f'Script execution failed with non-zero exit: {e.stderr.decode()}')
                return jsonify({'message': 'Error executing script', 'error': e.stderr.decode()}), 500

            except Exception as e:
                print(f'An unexpected error occurred: {str(e)}')
                return jsonify({'message': 'Unexpected error executing script', 'error': str(e)}), 500



        # print('Script executed successfully:', completed_linkedin_process.stdout.close())
        return jsonify({'message': 'Script executed successfully'})
    except subprocess.CalledProcessError as e:
        print(f'Script execution failed with non-zero exit: {e.stderr.decode()}')
        return jsonify({'message': 'Error executing script', 'error': e.stderr.decode()}), 500
    except Exception as e:
        print(f'An unexpected error occurred: {str(e)}')
        return jsonify({'message': 'Unexpected error executing script', 'error': str(e)}), 500
