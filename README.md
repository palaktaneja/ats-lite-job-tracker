# ATS Lite – Job Tracker Backend

This is a production-style backend system built to simulate a real Applicant Tracking System (ATS).

The goal of this project was not just to build CRUD APIs, but to design and scale a backend system the way it would exist in a real product environment.


## Project Does

- User registration and login with JWT authentication  
- Role-based access control (USER / ADMIN)  
- Job creation and management  
- Analytics service for reporting  
- Background task processing using Celery  
- Secure logout with token invalidation  


## Tech Stack

- **Flask** (Core API)
- **FastAPI** (Analytics microservice)
- **SQLAlchemy**
- **Redis** (Caching, rate limiting, token blacklist)
- **Celery** (Background jobs)
- **Docker & Docker Compose**
- **Flask-Migrate** (Database migrations)

## To run the Project

Make sure Docker is installed, then run:

```bash
docker-compose up --build