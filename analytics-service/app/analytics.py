from fastapi import APIRouter
from app.db import SessionLocal
from sqlalchemy import text
from app.schemas import JobsPerLocationResponse
from typing import List

router = APIRouter()


@router.get("/jobs-per-location", response_model=List[JobsPerLocationResponse])
def jobs_per_location():
    db = SessionLocal()

    result = db.execute(
        text("SELECT location, COUNT(*) as count FROM job GROUP BY location")
    )

    return [
        JobsPerLocationResponse(location=row[0], count=row[1])
        for row in result
    ]