from app.models.job import JobApplication
from app.core.extensions import db
from app.core.exceptions import NotFoundException

def create_job(title: str, description: str, location: str):
    job = JobApplication(
        title=title,
        description=description,
        location=location
    )

    db.session.add(job)
    db.session.commit()

    return job


def get_all_jobs():
    return JobApplication.query.all()


def get_job_by_id(job_id: int):
    job = JobApplication.query.get(job_id)
    if not job:
        raise NotFoundException("Job not found")

    return job