
from multiprocessing.managers import BaseManager

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


host_queue = Queue()
result_queue = Queue()
user_queue = Queue() #Queue will hold user requests

host = "localhost"
port = 50001
authkey = b"abc"

'''
    TODO
    Explore possibility of implementing the server as singleton

    On having a new Queue: finish crawling current host_queue or discard it?
'''
class QueueServer(BaseManager):
    def __init__(self):
        self.register('host_queue', callable=lambda: host_queue)
        self.register('result_queue', callable=lambda: result_queue)
        self.register('user_queue',callable=lambda :  user_queue)

        BaseManager.__init__(self, address=(host, port), authkey=authkey)

    # Method for getting one url-object
    def getURl(self):
        if not user_queue.empty():
            return user_queue.get()

        return host_queue.get()

    #Will empty the server_queue
    def empty_queue(self):
        # two possibilities: emptying with a loop or garbage collection
        #host_queue = Queue()
        while(not host_queue.empty()):
            host_queue.get()

    def useNewList(self,*newList):
        self.empty_queue()
        for item in newList:
            host_queue.put(item)


# End of QueueServer class


class QueueClient(BaseManager):
    def __init__(self):
        self.register('host_queue')
        self.register('result_queue')
        self.register('user_queue')
        BaseManager.__init__(self, address=(host, port), authkey=authkey)
        self.connect()