from RedisQ.usage.jobs import *
from RedisQ.usage.WSIWorker import WSIWorker, PlayLoadConfig
from redis import Redis
from RedisQ.Qlist import LQ, LW, LD, HS
import requests
from WSI.algorithm.code import *
from time import time

# def my_work_list(LW):
#     id = "1"
#     list_name = 'worklist_' + id


def playload(job, config):
    print('playload running...')
    # get job
    content = job.content
    # get api information
    print('get resource info')
    response = requests.get(content.api + content.image)
    if response.status_code != 200:
        return
    print('download raw file')
    raw_uri = response.json().get('raw_file_path', None)
    response = requests.get(raw_uri)
    if response.status_code != 200:
        return
    print('ready to predict')
    filename = response.url.split('/')[-1]
    # set file path
    res = '{base}/{filename}'.format(
        base=config.res_base,
        filename=filename
    )

    des = '{base}/{time}'.format(
        base=config.des_base,
        time=time()
    )
    # write content
    with open(res, 'wb+') as f:
        f.write(response.content)
    print('prediction...')
    # run algorithm
    predict_one_wsi(res, des)
    # TODO write result infomation here


def playload_build(config):
    # args = {
    #     'path': config.docker_path,
    #     'tag': config.docker_image_tag,
    # }
    # try:
    #     print('getting...')
    #     print(docker_client.images.list())
    #     docker_client.images.get(config.docker_image_tag)
    # except docker.errors.ImageNotFound:
    #     print('building...')
    #     docker_client.images.build(**args)
    print('build')


def main(host, port):
    conn = Redis(host=host, port=port)
    config = PlayLoadConfig()
    worker = WSIWorker(connection=conn, config=config,sign_hash=HS,
                       queue_list=LQ, working_list=LW, done_list=LD)
    # playload_build(config)
    print('polling...')
    worker.polling(config=config, playload=playload)

if __name__ == '__main__':
    main(host='192.168.0.110', port='6389')
