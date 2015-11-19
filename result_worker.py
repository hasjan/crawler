
from queue_manager import QueueClient


if __name__ == "__main__":

    # get instance of QueueClient
    c = QueueClient()

    # get appropriate queue from QueueClient
    qm = c.queue_manager()

    while True:
        result = qm.next_result()

        print(result.keys())
        # do something with result ...
        print(result["target"])
        print(result)

