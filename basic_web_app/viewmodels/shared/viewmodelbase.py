from typing import Optional

import flask
from flask import Request

from basic_web_app.infrastructure import ( request_dict, instance as localhost)



class ViewModelBase:
    def __init__(self):
        instance = localhost.Data()
        self.request: Request = flask.request
        self.request_dict = request_dict.create("")
        self.instance_id: str = instance.get_instance_id()
        self.region: str = instance.get_region()
        self.tags: dict = instance.get_tags()
        self.db_endpoint: str = instance.get_database_endpoint()
        self.error: Optional[str] = None

    def to_dict(self):
        return self.__dict__
