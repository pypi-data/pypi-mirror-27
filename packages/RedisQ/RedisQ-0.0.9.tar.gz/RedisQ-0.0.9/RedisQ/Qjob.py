from time import time


class BaseJob(object):
    """if you want to create a new job just extend this class"""
    source = None
    destination = None
    content = None
    status_change = {}
    _status = None

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
    content =  PredictionContent()