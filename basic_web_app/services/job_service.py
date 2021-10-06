from flask import request
from typing import Optional
from datetime import datetime, timedelta, timezone
from basic_web_app import db
from basic_web_app.data.jobs import JobsTable
from basic_web_app.infrastructure import instance


class JobsPage:
    def __init__(self):
        self.localhost = instance.Data()
        self.init_job_data()

    def init_job_data(self):
        self.job_data = JobsTable.query.all()

    def set_job(self, r):

        if self.validate_job(r):
            return self.create_job(r)
        else:
            return False

    def validate_job(self, r: request):

        name = r.form.get("name", type=str)
        employer = r.form.get("employer", type=str)
        salary = r.form.get("salary", type=str).strip("$ ")
        description = r.form.get("description", type=str)

        if not name or not employer or not salary or not description:
            print("Stuff is missing")
            return False
        else:
            print("All checks out")
            return True

    def create_job(self, r: request) -> Optional[JobsTable]:

        new_job = JobsTable(
            name=r.form.get("name", type=str),
            employer=r.form.get("employer", type=str),
            salary=r.form.get("salary", type=str).strip("$ "),
            description=r.form.get("description", type=str),
            created_date=datetime.now(tz=timezone(timedelta(hours=10))),
        )

        try:
            db.session.add(new_job)
            db.session.commit()
        finally:
            self.init_job_data()
            db.session.close()

        return True

    def get_jobs_data(self):
        return self.job_data

    def get_job_page_data(self) -> dict:

        data = {"localhost": self.localhost, "jobs": self.get_jobs_data()}

        return data

    def post_job_page_data(self, request_data):

        data = {
            "localhost": self.localhost,
            "new_job": self.set_job(request_data),
            "jobs": self.get_jobs_data(),
        }

        return data
