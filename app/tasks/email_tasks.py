from app.tasks.celery_app import celery


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_job_notification(self, job_title):
    print(f"Sending email notification for job: {job_title}")