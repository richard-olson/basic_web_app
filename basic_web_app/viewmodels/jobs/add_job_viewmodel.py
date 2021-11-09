from typing import Optional

from basic_web_app.viewmodels.shared.viewmodelbase import ViewModelBase


class AddJobViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.name: Optional[str] = None
        self.employer: Optional[str] = None
        self.salary: Optional[int] = None
        self.description: Optional[str] = None
        self.created: Optional[str] = None

    def form_data(self):
        d = self.request_dict
        self.name = d.get("name")
        self.employer = d.get("employer")
        self.description = d.get("description")
        self.salary = d.get("salary")


    def validate(self):
        if not self.name or not self.name.strip():
            self.error = "You must specify a name."
        elif not self.employer or not self.employer.strip():
            self.error = "You must specify an employer."
        elif not self.salary:
            self.error = "You must specify a salary."
        elif not self.description or not self.description.strip():
            self.error = "You must specify a description."

        if self.salary:
            try:
                self.salary = int(self.salary.replace(",", ""))
            except:
                self.error = "Salary must be a number."
    
    