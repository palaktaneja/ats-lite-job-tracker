from app.models.job import JobApplication
from app.core.extensions import db
from app.core.exceptions import NotFoundException
import json
from app.core.redis_client import get_redis_client

def create_job(title: str, description: str, location: str):
    job = JobApplication(
        title=title,
        description=description,
        location=location
    )

    db.session.add(job)
    db.session.commit()

    # Invalidate cache after DB change
    redis_client = get_redis_client()
    redis_client.delete("all_jobs")
    return job


def get_all_jobs():
    redis_client = get_redis_client()

    cached_jobs = redis_client.get("all_jobs")

    if cached_jobs:
        return json.loads(cached_jobs)

    jobs = JobApplication.query.all()

    job_list = [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location
        }
        for job in jobs
    ]

    redis_client.setex("all_jobs", 60, json.dumps(job_list))  # cache 60 seconds

    return job_list


def get_job_by_id(job_id: int):
    job = JobApplication.query.get(job_id)
    if not job:
        raise NotFoundException("Job not found")

    return job