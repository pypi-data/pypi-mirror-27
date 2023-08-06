from redis import Redis
from Qjob import BaseJob
from Qlist import LD,LW,LQ
conn = Redis(host='127.0.0.1',port='6379')

ld = LD(connection=conn)
lw = LW(connection=conn)
lq = LQ(connection=conn)

job = BaseJob()

lq.queue(job)
print(lq.get(0))
lq.pop_to(lw)
print(lw.get(0))
lw.pop_to(ld)
print(l.get(0))