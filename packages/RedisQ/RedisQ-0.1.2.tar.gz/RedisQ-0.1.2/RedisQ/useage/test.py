from RedisQ.Qlist import LQ,LD,LS
from redis import Redis
from RedisQ.Qjob import BaseJob
from RedisQ.useage.jobs import WSIJob
import time
conn = Redis(host='192.168.0.110', port='6389')

for _ in range(2):
    job = WSIJob()
    lq = LQ(connection = conn)
    lq.queue(job)

while True:
    ld = LD(connection=conn)
    ls = LS(connection=conn)
    lq = LQ(connection=conn)
    print('queue work {}'.format(lq.len()))
    print('woring workers {}'.format(ls.len()))
    print('done work {}'.format(ld.len()))
    print('=================')
    time.sleep(5)