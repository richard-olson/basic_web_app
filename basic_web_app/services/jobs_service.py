from typing import Optional
from datetime import datetime, timedelta, timezone
from basic_web_app import db
from basic_web_app.data.jobs import Job


def get_job_data():
    try:
        return Job.query.all()
    except Exception as error:
        return error


def create_job(
    name: str, employer: str, salary: int, description: str
) -> Optional[Job]:

    new_job = Job(
        name=name,
        employer=employer,
        salary=salary,
        description=description,
        created_date=datetime.now(tz=timezone(timedelta(hours=10))),
    )

    try:
        db.session.add(new_job)
        db.session.commit()
    finally:
        db.session.close()

    return Job
