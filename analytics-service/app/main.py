from fastapi import FastAPI
from app.analytics import router

app = FastAPI(title="ATS Analytics Service")

app.include_router(router, prefix="/analytics")