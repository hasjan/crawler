"""
This module fetches results out of the queue_manager and formats it in JSON to add it to da database
"""


from queue_manager import QueueClient
from pymongo import MongoClient, errors
from time import sleep
import datetime
from tld import get_tld


class Database(object):
    """
    This is the database wrapper class.
    An instance of it holds the connection to the Database and contains methods
    for operations on the Database.
    """

    def __init__(self):
        self.db_client = MongoClient('localhost', 27017)
        self.db = self.db_client.tls_crawler
        self.coll = self.db.tls_scan_results

    def insert_result(self, query, append):
        """
        Putting result to The Database.
        Appends the new Scan if the given query matches an existing document.
        Otherwise it creates a new one.

        :param query: query to search for an existing document.
        :param append: the result of the current scan.
        :return:
        """
        # retry the insert, if the connection to the database is lost
        for i in range(60):
            try:
                self.coll.update(query, append, upsert=True)
                break
            except errors.AutoReconnect as e:
                print e
                sleep(5)
        else:
            raise Exception("Could not insert!")
        return


def main():
    # get instance of QueueClient
    c = QueueClient()
    # get appropriate queue from QueueClient
    qm = c.queue_manager()
    # get instance of Database
    mdb = Database()

    while True:
        result = qm.next_result()

        # get tld suffix. tld installed with 'pip install tld'
        # to update the tld-names run 'update-tld-names' as discribed in https://pypi.python.org/pypi/tld
        tld = get_tld('https://' + result["target"][0], as_object=True).suffix

        # fill cs_avail and cs_pref with the cipher suites of the result
        cs_avail = []
        cs_pref = []
        tls_ver = ['tlsv1_2', 'tlsv1_1', 'sslv3', 'sslv2', 'tlsv1']

        for k in range(5):
            if 'preferredCipherSuite' in (result['result'][k]):
                for cs, value in ((result['result'][k])['preferredCipherSuite']).iteritems():
                    if value[2]:
                        cs_pref.append('{ '
                                       'cs: ' + cs + ', tls_version: ' + tls_ver[k] +
                                       ', dh_param : ' + value[2]['GroupSize'] + ' }')
                    else:
                        cs_pref.append('{ cs: ' + cs + ', tls_version: ' + tls_ver[k] + ' }')

                for cs, value in ((result['result'][k])['acceptedCipherSuites']).iteritems():
                    if value[2]:
                        cs_avail.append('{ cs: ' + cs + ', tls_version: ' + tls_ver[k] +
                                        ', dh_param : ' + value[2]['GroupSize'] + ' }')
                    else:
                        cs_avail.append('{ cs: ' + cs + ', tls_version: ' + tls_ver[k] + ' }')

        update_query = {
            'domain:': result["target"][0],
            'tld': tld,
        }
        # check whether a preferred cs is available. Otherwise the host was not accessible
        if cs_pref:
            update_add = {
                "$addToSet": {"scans": {
                    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': result["source"],
                    'cs_pref': cs_pref,
                    'cs_avail': cs_avail,
                }}
            }

            mdb.insert_result(update_query, update_add)

if __name__ == "__main__":
    main()
