
from queue_manager import QueueClient


if __name__ == "__main__":

    # get instance of QueueClient
    c = QueueClient()

    # get appropriate queue from QueueClient
    result_queue = c.result_queue()

    while True:
        result = result_queue.get()

        # do something with result ...
        print(result)

