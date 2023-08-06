from RedisQ.Qlist import LQ,LD,LW
from redis import Redis
from RedisQ.Qjob import BaseJob
import time
conn = Redis(host='192.168.0.110', port='6389')


class WSIPredictionContent(object):

    api = 'http://192.168.0.110:8000/api/v1/'
    patient = 'patients/1/'
    case = 'cases/2351cb63-ea0a-4f40-8fed-5a82761adb7e/'
    accession = 'accessions/1/'
    image = 'images/1/'

class WSIJob(BaseJob):
    
    content = WSIPredictionContent()

class DICOMJob(BaseJob):
    pass