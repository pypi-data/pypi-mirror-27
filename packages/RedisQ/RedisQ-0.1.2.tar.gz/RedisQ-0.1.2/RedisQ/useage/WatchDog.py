
# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify
import pickle
import functools
wm = pyinotify.WatchManager()  # Watch Manager
watch_dir_name = 'workout'
watch_dir = './{0}/'.format(watch_dir_name)

class EventHandler(pyinotify.ProcessEvent):

    def is_metadata_create(self, event):
        if event.pathname.split('/')[-3] == watch_dir_name and event.name.endswith('metadata'):
            return True
        return False

    def parse_metadata(self, event):
        with open(event.pathname,'rb') as f:
            metadata = pickle.load(f)
        return metadata

    def upload(self, type, filename):
        #TODO upload to api
        pass

    def process_IN_CREATE(self, event):
        # 等待metadata结果写入
        if is_metadata_create(event):
            # 解析metadata
            metadata = parse_metadata(event)
            for type, filename in metadata.files:
                # 获取各个文件
                with open(filename,'r') as f:
                    upload(type, file) 
                # 上传到后端
        print("Create:{0}".format(event.pathname))

    def process_IN_DELETE(self, event):
        print("Removing:{0}".format(event.pathname))


def on_loop(notifier):
    """
    Dummy function called after each event loop, this method only
    ensures the child process eventually exits (after 5 iterations).
    """
    pass


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(watch_dir, pyinotify.ALL_EVENTS)
notifier.loop()
# on_loop_func = functools.partial(on_loop)

# try:
#     notifier.loop(daemonize=True, callback=on_loop_func,
#                   pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
# except pyinotify.NotifierError as err:
#     print >> sys.stderr, err
