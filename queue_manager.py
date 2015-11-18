
from multiprocessing.managers import BaseManager

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


host_queue = Queue()
result_queue = Queue()
user_queue = Queue()  #Queue will hold user requests

host = "localhost"
port = 50001
authkey = b"abc"

''' TODO
    On having a new Queue: finish crawling current host_queue or discard it?'''


# This class will offer several methods to ease the use of the three queues
class HostQueueClass(object):
    def __init__(self):
        pass

    # Method for getting one url-object. user_queue is prioritized.
    # Every item polled from host_queue will be appended at the end of the same queue
    def getUrl(self):
        if not user_queue.empty():
            return user_queue.get()
        item = host_queue.get()
        host_queue.put(item)
        return item

    #This will discard the old queue and add new items from a supplied list
    def useNewList(self,newList):
        host_queue = Queue()
        for item in newList:
            host_queue.put(item)

    def putResult(self,result):
        result_queue.put(result)

    # Add user url to user_queue
    def putUserRequest(self,request):
        user_queue.put(request)

# End of HostQueueClass class

worker = HostQueueClass()

class QueueServer(BaseManager):
    def __init__(self):
        self.register('host_queue', callable=lambda: host_queue)
        self.register('result_queue', callable=lambda: result_queue)
        self.register('user_queue', callable=lambda :  user_queue)
        #Lambda statement important: class is not callable by itself
        self.register('HostQueueClass', callable=lambda: worker)

        BaseManager.__init__(self, address=(host, port), authkey=authkey)

# End of QueueServer class


class QueueClient(BaseManager):
    def __init__(self):
        self.register('host_queue')
        self.register('result_queue')
        self.register('user_queue')
        self.register('HostQueueClass')
        BaseManager.__init__(self, address=(host, port), authkey=authkey)
        self.connect()

# End of QueueClient class
