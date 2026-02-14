from flask import request, Blueprint
from app.api.v1.schemas.job_schema import JobCreateSchema, JobResponseSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from app.api.v1.dependencies import role_required


job_create_schema = JobCreateSchema()
job_response_schema = JobResponseSchema()
jobs_response_schema = JobResponseSchema(many=True)

from app.services.job_service import (
    create_job,
    get_all_jobs,
    get_job_by_id
)

job_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

@job_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def add_job():
    data = job_create_schema.load(request.get_json())
    job = create_job(**data)
    
    return job_response_schema.dump(job), 201


@job_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = get_all_jobs()
    return jobs_response_schema.dump(jobs)


@job_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = get_job_by_id(job_id)

    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location
    }