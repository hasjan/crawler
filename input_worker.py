from queue_manager import QueueClient

__author__ = 'david'


if __name__ == "__main__":

    # get instance of QueueClient
    c = QueueClient()

    # get appropriate queue from QueueClient
    qm = c.queue_manager()


    qm.put_new_list(
        [
            [
                "google.com", ["alexa-top-1m"],
            ],

            [
                "facebook.com", ["alexa-top-1m"],
            ],

            [
                "sadsafcsdsadsa.com", ["alexa-top-1m"],
            ]
        ]
    )



