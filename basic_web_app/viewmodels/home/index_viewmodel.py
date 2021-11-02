from basic_web_app.services import home_service
from basic_web_app.viewmodels.shared.viewmodelbase import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.localhost = home_service.get_localhost_data()
        self.ec2_data = home_service.get_ec2_data(self.localhost)
        self.ec2_health = home_service.get_ec2_health_data(self.localhost, self.ec2_data)
        self.asg = home_service.get_asg_data(self.localhost, self.ec2_data)
        self.targetgroup = home_service.get_alb_data(self.localhost, self.asg)
        self.db_id = home_service.get_db_id_data()
        self.rds = home_service.get_rds_data(self.localhost)
        self.cloudwatch = home_service.get_cloudwatch_data(self.localhost)
        self.diagnostic = home_service.get_diagnostic_mode(self.request_dict)