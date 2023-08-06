from RedisQ.Base.Qlist import LW, LQ
from RedisQ.Base.Qjob import PredictionJob, PredictionContent
from RedisQ.BaseWorker import BaseWorker
#import GPUtil as gpu


class GPUWorker(BaseWorker):
    """docstring for WSIWorker"""

    def management(self, payload, config):
        # TODO get system info and decide need to work
        if self.working_list.len() > 0:
            job = self.working_list.get(0)
        else:
            job = self.queue_list.pop_to(self.working_list)
        if not job:
            raise Exception('can not get a job instance')
#        gpus = gpu.getGPUs()
#        availability = gpu.getAvailability(gpus, maxLoad=self.config.gpu_load,
 #                                                maxMemory=self.config.gpu_memory)
        availability = True
        if availability:
            payload(job, config)
        else:
            self.working_list.re_queue(self.queue_list)

