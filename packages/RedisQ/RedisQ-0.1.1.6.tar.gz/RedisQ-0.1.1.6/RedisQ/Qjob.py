from time import time
from uuid import uuid1


class BaseJob(object):
    """if you want to create a new job just extend this class"""
    id = None
    source = None
    destination = None
    content = None
    status_change = {}
    _status = None

    def __init__(self):
        self.id = uuid1()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self.status_change.update({value: time()})
        self._status = value


class PredictionContent(object):
    """the content class for Prediction Job"""
    args = {}


class PredictionJob(BaseJob):
    """the particular job for Deep Learning Prediction"""
    content = PredictionContent()
