from typing import Optional

from basic_web_app.viewmodels.shared.viewmodelbase import ViewModelBase
from basic_web_app.services.jobs_service import create_random_jobs


class RandomJobViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        d = create_random_jobs()
        self.name = d.get("new_job")
        self.employer = d.get("new_employer")
        self.salary = d.get("new_salary")
        self.description = d.get("new_description")