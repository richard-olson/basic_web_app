import random
from typing import Optional
from datetime import datetime, timedelta, timezone
from basic_web_app import db
from basic_web_app.data.jobs import Job
import basic_web_app.data.random_jobs as random_jobs


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

def delete_job(id: str):
    
    job = Job.query.filter_by(id=id).one()

    try:
        db.session.delete(job)
        db.session.commit()
    finally:
        db.session.close()

def delete_all_jobs():
    
    try:
        db.session.query(Job).delete()
        db.session.commit()
    finally:
        db.session.close()

def create_random_jobs():

    random_job = {}
    random_job["new_job"] = random.choice(random_jobs.names)
    random_job["new_employer"] = random.choice(random_jobs.employers)
    random_job["new_salary"] =  random.randrange(10000, 1000000, 1000)
    random_job["new_description"] = f"Working as a {random_job['new_job']} at {random_job['new_employer']} sounds like great fun."

    return random_job