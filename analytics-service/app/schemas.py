from pydantic import BaseModel


class JobsPerLocationResponse(BaseModel):
    location: str
    count: int