from celery import Celery
import os


def make_celery():
    celery = Celery(
        "ats",
        broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    )

    return celery


celery = make_celery()