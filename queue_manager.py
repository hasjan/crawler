
from multiprocessing.managers import BaseManager

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


host_queue = Queue()
result_queue = Queue()

host = "localhost"
port = 50001
authkey = b"abc"


class QueueServer(BaseManager):
    def __init__(self):
        self.register('host_queue', callable=lambda: host_queue)
        self.register('result_queue', callable=lambda: result_queue)

        BaseManager.__init__(self, address=(host, port), authkey=authkey)



class QueueClient(BaseManager):
    def __init__(self):
        self.register('host_queue')
        self.register('result_queue')
        BaseManager.__init__(self, address=(host, port), authkey=authkey)
        self.connect()
