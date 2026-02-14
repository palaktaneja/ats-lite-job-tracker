from flask import request, Blueprint
from app.services.job_service import (
    create_job,
    get_all_jobs,
    get_job_by_id
)

job_bp = Blueprint("jobs", __name__, url_prefix="/jobs")
@job_bp.route("/", methods=["POST"])
def add_job():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    location = data.get("location")

    if not title:
        return {"error": "Title is required"}, 400

    job = create_job(title, description, location)

    return {
        "id": job.id,
        "title": job.title
    }, 201


@job_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = get_all_jobs()

    return [
        {
            "id": job.id,
            "title": job.title,
            "location": job.location
        }
        for job in jobs
    ]


@job_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = get_job_by_id(job_id)

    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location
    }