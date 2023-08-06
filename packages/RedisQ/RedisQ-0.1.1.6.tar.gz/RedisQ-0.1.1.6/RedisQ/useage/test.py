from RedisQ.Qlist import LQ,LD,LW
from redis import Redis
from RedisQ.Qjob import BaseJob
from Redis.useage.jobs import WSIJob
import time
conn = Redis(host='192.168.0.110', port='6389')

for _ in range(2):
    job = WSIJob()
    lq = LQ(connection = conn)
    lq.queue(job)

while True:
    ld = LD(connection=conn)
    lw = LW(connection=conn)
    lq = LQ(connection=conn)
    print('queue work {}'.format(lq.len()))
    print('woring work {}'.format(lw.len()))
    print('done work {}'.format(ld.len()))
    print('=================')
    time.sleep(5)