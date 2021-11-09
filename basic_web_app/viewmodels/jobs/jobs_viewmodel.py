from basic_web_app.services import jobs_service
from basic_web_app.viewmodels.shared.viewmodelbase import ViewModelBase


class JobsViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        
        self.jobs = jobs_service.get_job_data()
