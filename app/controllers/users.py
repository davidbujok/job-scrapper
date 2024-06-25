import json
import os
import subprocess
from flask import Blueprint, jsonify
from app.models.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/<id>", methods=['GET', 'POST'])
def get_all_jobs(id):
    all_jobs = User.get_user_jobs(id)
    return json.dumps(all_jobs, default=str)

