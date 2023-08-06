from RedisQ.Qlist import LW, LQ
from RedisQ.Qjob import PredictionJob, PredictionContent
from BaseWorker import BaseWorker
import GPUtil as gpu


class PlayLoadConfig(object):

    gpu_load = 0.3
    gpu_memory = 0.3
    docker_path = './test'
    docker_image_tag = 'test_work'
    res_base = 'WSI/res'
    des_base = 'WSI/des'

    @property
    def gpu_fraction(self):
        return (self.gpu_memory + self.gpu_load) * 0.5


class WSIWorker(BaseWorker):
    """docstring for WSIWorker"""

    def management(self, playload, config):
        # TODO get system info and decide need to work
        if self.working_list.len() > 0:
            job = self.working_list.get(1)
        else:
            job = self.queue_list.pop_to(self.working_list)
        if not job:
            return
        gpus = gpu.getGPUs()
        availability = gpu.getAvailability(gpus, maxLoad=self.config.gpu_load,
                                           maxMemory=self.config.gpu_memory)
        if availability:
            playload(job, config)
        else:
            self.working_list.re_queue(self.queue_list)

