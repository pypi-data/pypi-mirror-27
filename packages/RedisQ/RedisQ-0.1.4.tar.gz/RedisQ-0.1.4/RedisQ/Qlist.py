from redis import Redis
import pickle
from io import BytesIO


class BaseList(object):
    """if you want to create a new list just extend this class"""
    conn = None
    list_name = __name__

    def __init__(self, connection=None, list_name=None):
        assert connection is not None, "the redis connection is required"

        self.conn = connection
        if list_name:
            self.list_name = list_name

    def __iter__(self):
        return self

    def __next__(self):
        if self.len() > 0:
            ret = self.pop()
            return ret
        else:
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
                return pickle.loads(ret)
        return None

    def pop(self):
        return pickle.loads(self.conn.lpop(self.list_name))

    def pull(self):
        return pickle.loads(self.conn.rpop(self.list_name))

    def re_queue(self, another_list):
        job = another_list.pull()
        job = pickle.dumps(job)
        self.conn.lpush(self.list_name, job)

    def set(self, index, job):
        job = pickle.dumps(job)
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


class HS(object):
    """the hash of holding sign workers worker:working list"""
    hash_name = 'sign_hash'
    conn = None

    def __init__(self, connection=None, hash_name=None):
        assert connection is not None, "the redis connection is required"
        self.conn = connection
        if hash_name:
            self.hash_name = hash_name

    def sign_in(self, worker, list):
        self.conn.hset(self.hash_name, worker.id, list.id)

    def sign_out(self, worker, list):
        self.conn.hget(self.hash_name, worker.id)

class LQ(BaseList):
    """the list of holding queue jobs"""
    list_name = 'queue_list'


class LW(BaseList):
    """the list of holding working jobs"""
    list_name = 'work_list'


class LD(BaseList):
    """the list of holding done jobs"""
    list_name = 'done_list'
