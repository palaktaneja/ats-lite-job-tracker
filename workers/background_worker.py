import threading
import time

def send_reminder(job_id, user_id):
    def task():
        print(f"[WORKER] Sending reminder for job {job_id} to user {user_id}")
        time.sleep(5)
        print(f"[WORKER] Reminder sent for job application {job_id} for user {user_id}")

    thread= threading.Thread(target=task)
    thread.start()