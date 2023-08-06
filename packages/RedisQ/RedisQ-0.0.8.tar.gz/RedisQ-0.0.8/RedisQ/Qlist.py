from redis import Redis
import pickle
from io import BytesIO


class BaseList(object):
    """if you want to create a new list just extend this class"""
    conn = None
    list_name = __name__
    i = 0

    def __init__(self, connection=None, list_name=None):
        assert connection is not None, "the redis connection is required"

        self.conn = connection
        if list_name:
            self.list_name = list_name

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.len():
            ret = self.get(self.i)
            self.i += 1
            return ret
        else:
            i = 0
            raise StopIteration()

    def queue(self, job):
        """queues a job into this list"""
        # TODO serializer job
        job.status = "queue into {0}".format(self.list_name)
        job = pickle.dumps(job)
        self.conn.lpush(self.list_name, job)

    def pop_to(self, another_list):
        """moves the least job from this list into another list """
        job = self.get(-1)
        if job:
            job.status = 'move form {this_list} into {list_name}'.format(
                this_list=self.list_name,
                list_name=another_list.list_name)
            self.set(-1, job)
            ret = self.conn.rpoplpush(self.list_name, another_list.list_name)
            if ret is not None:
                return ret
        return None

    def pop(self):
        """returns and moves the least job from this list"""
        return self.conn.rpop(self.list_name)

    def set(self, index, job):
        job = pickle.dumps(job)
        # TODO 一致性验证
        self.conn.lset(self.list_name, index, job)

    def get(self, index):
        """returns the job from this list at the index"""
        job = self.conn.lindex(self.list_name, index)
        if job:
            return pickle.loads(job)
        else:
            return None

    def len(self):
        return self.conn.llen(self.list_name)


class LQ(BaseList):
    """the list of holding queue jobs"""
    list_name = 'queue_list'


class LW(BaseList):
    """the list of holding working jobs"""
    list_name = 'work_list'


class LD(BaseList):
    """the list of holding done jobs"""
    list_name = 'done_list'
