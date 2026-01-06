from extensions import db
from datetime import datetime

class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id= db.Column(db.Integer, primary_key=True)
    company= db.Column(db.String(100), nullable=False)
    role= db.Column(db.String(100), nullable=False)
    status= db.Column(db.String(50), default="Applied")
    applied_date= db.Column(db.DateTime, default=datetime.utcnow)
    notes= db.Column(db.Text)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<JobApplication {self.id}: {self.company} - {self.role}>"