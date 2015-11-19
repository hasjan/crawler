"""
This module ...
"""


from queue_manager import QueueClient
from pymongo import MongoClient, errors
from time import sleep


class Database(object):

    def __init__(self):
        self.db_client = MongoClient('localhost', 27017)
        self.db = self.db_client.tls_crawler
        self.coll = self.db.tls_scan_results

    def insert_result(self, db_input):
        # retry the insert, if the connection to the database is lost
        for i in range(60):
            try:
                self.coll.insert_one(db_input)
                break
            except errors.AutoReconnect as e:
                print e
                sleep(5)
        else:
            raise Exception("Could not insert!")
        return

if __name__ == "__main__":

    # get instance of QueueClient
    c = QueueClient()

    # get appropriate queue from QueueClient
    qm = c.queue_manager()

    # get instance of Database
    mdb = Database()

    while True:
        result = qm.next_result()

        # do something with result ...

        # mdb.insert_result({"test": "test"})
        # print(result.keys())
        # print(result["target"])
        # print(result)
