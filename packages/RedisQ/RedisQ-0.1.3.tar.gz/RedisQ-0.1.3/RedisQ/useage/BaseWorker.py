import uuid
import os
import daemon
pid_file = 'worker.pid'
class BaseWorker(object):
    """docstring for BaseWorker"""
    conn = None
    config = None
    queue_list = None
    working_list = None
    done_list = None
    sign_hash = None
    id = None

    def __init__(self, connection=None, config=None, sign_hash=None, queue_list=None, working_list=None, done_list=None):
        if connection:
            self.conn = connection
            self.id = uuid.uuid1()
            self.queue_list = queue_list(self.conn)
            self.working_list = working_list(
                connection=self.conn, list_name='work_list_{}'.format(self.id))
            self.sign_hash = sign_hash(self.conn)
            self.sign_hash.sign_in(self, self.working_list)
            self.done_list = done_list(self.conn)
        if config:
            self.config = config
        if os.path.isfile(pid_file):
            #宣告前任死亡,继承前任的工作
            with open(pid_file,'r') as f:
                id = f.read()
                dead_working_list = working_list(self.conn,'work_list_{}'.format(id))
                dead_working_list.id = id
                for job in dead_working_list:
                    self.working_list.queue(job)
                self.sign_hash.sign_out(dead_working_list)

        with open(pid_file,'w+') as f:
            f.write(str(self.id))

    def polling(self, playload=None, config=None):
        try:
            with daemon.DaemonContext():
                while True:
                    if self.working_list.len() > 0 or self.queue_list.len() > 0:
                        self.management(playload, config)
        except KeyboardInterrupt as e:
            os.remove(pid_file)
            self.sign_hash.sign_out(self)
             
        

    def management(self, playload, config):
        # for Atomicity isuses
        # it should be pop_to then jugde the availablility
        # if not then push back./
        # job = self.queue_list.pop_to(self.working_list)
        # if job:
        #     availability = True
        #     if availability:
        #         playload(job, config)
        # else:
        #     print('playload out')
        raise NotImplementedError('management should implement')
