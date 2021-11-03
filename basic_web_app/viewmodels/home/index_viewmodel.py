from basic_web_app.services import home_service
from basic_web_app.viewmodels.shared.viewmodelbase import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.ec2_data    = home_service.get_ec2_data(self.region, self.tags)
        self.ec2_health  = home_service.get_ec2_health_data(self.region, self.ec2_data)
        self.asg         = home_service.get_asg_data(self.region, self.ec2_data)
        self.targetgroup = home_service.get_alb_data(self.region, self.asg)
        self.db_id       = home_service.get_db_id_data()
        self.rds         = home_service.get_rds_data(self.region, self.db_endpoint)
        self.cloudwatch  = home_service.get_cloudwatch_data(self.region, self.tags)
        self.diagnostic  = home_service.get_diagnostic_mode(self.request_dict)
