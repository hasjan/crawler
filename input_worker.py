from queue_manager import QueueClient

__author__ = 'david'


if __name__ == "__main__":

    # get instance of QueueClient
    c = QueueClient()

    # get appropriate queue from QueueClient
    host_queue = c.queue_manager()
    print host_queue

    # for i in range(20):
    #     # put hostname to host_queue
    #     host_queue.put("google.com")


