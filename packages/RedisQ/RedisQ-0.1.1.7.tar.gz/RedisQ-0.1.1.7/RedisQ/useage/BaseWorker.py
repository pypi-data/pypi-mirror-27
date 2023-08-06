import uuid

class BaseWorker(object):
    """docstring for BaseWorker"""
    conn = None
    config = None
    queue_list = None
    working_list = None
    done_list = None
    id = None

    def __init__(self, connection=None, config=None, queue_list=None, working_list=None, done_list=None):
        if connection:
            self.conn = connection
            self.id = uuid.uuid1()
            self.queue_list = queue_list(self.conn)
            self.working_list = working_list(connection=self.conn, list_name='work_list_{}'.format(self.id))
            self.done_list = done_list(self.conn)
        if config:
            self.config = config

    def polling(self, playload=None, config=None):
        while True:
            if self.queue_list.len() > 0:
                self.management(playload, config)

    def management(self, playload, config):
        # for Atomicity isuses 
        # it should be pop_to then jugde the availablility
        # if not then push back./
        job = self.queue_list.pop_to(self.working_list)
        if job:
            availability = True
            if availability:
                playload(job, config)
        else:
            print('playload out')