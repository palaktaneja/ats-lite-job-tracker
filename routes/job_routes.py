from flask import Blueprint, request, jsonify
from extensions import db
from models.job import JobApplication

job_bp= Blueprint("jobs", __name__, url_prefix="/jobs")

@job_bp.route("", methods= ["POST"])
def create_job():
    data= request.get_json()

    company= data.get("company")
    role = data.get("role")
    status = data.get("status", "Applied")
    notes = data.get("notes")

    if not company or not role:
        return {"error": "Comapny and role required"}, 400
    
    job= JobApplication(
        company=company,
        role=role,
        status=status,
        notes=notes
    )
    db.session.add(job)
    db.session.commit()
    return {"message": "Job application created successfully", "job_id": job.id}, 201

@job_bp.route("", methods=["GET"])
def get_all_jobs():
    jobs= JobApplication.query.all()

    result= []
    for job in jobs:
        result.append({
            "id": job.id,
            "company": job.company,
            "role": job.role,
            "status": job.status,
            "notes": job.notes
        })
    return jsonify(result), 200
