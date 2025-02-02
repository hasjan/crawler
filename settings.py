"""
This module contains global settings for all modules.
"""


#: the bind address of the :class:`~queue_manager.QueueServer`
SERVER_ADDRESS = 'localhost'

#: the bind port of the :class:`~queue_manager.QueueServer`
SERVER_PORT = 50001

#: the authentication string of the :class:`~queue_manager.QueueServer`
SERVER_AUTH = b'abc'


#: the number of sslyze worker processes
NUMBER_PROCESSES = 1

#: a list of commands that sslyze will be used for scanning.
#:  available commands are:
#:      ["tlsv1_2", "tlsv1_1", "tlsv1", "sslv3", "sslv2", "reneg", "hsts", "resum", "resum_rate",
#:      "heartbleed", "chrome_sha1", "compression", "certinfo"]
#: For details see `SSLyze <https://github.com/nabla-c0d3/sslyze>`_.
COMMAND_LIST = [
    "tlsv1_2",
    "tlsv1_1",
    "tlsv1",
    "sslv3",
    "sslv2",
    # "reneg",
    # "hsts",
    # "resum",
    # "resum_rate",
    # "heartbleed",
    # "chrome_sha1",
    # "compression",
    # "certinfo",
]



#: this are shared settings used by sslyze.
#:   For details see `SSLyze <https://github.com/nabla-c0d3/sslyze>`_.
SHARED_SETTINGS = {
    'ca_file': None,
    'certinfo': 'basic',
    'starttls': None,
    'resum': True,
    'resum_rate': None,
    'http_get': True,
    'xml_file': None,
    'compression': True,
    'tlsv1': True,
    'targets_in': None,
    'keyform': 1,
    'hsts': None,
    'chrome_sha1': None,
    'sslv3': True,
    'sslv2': True,
    'https_tunnel': None,
    'nb_retries': 4,
    'heartbleed': True,
    'sni': None,
    'https_tunnel_host': None,
    'regular': False,
    'key': None,
    'reneg': True,
    'tlsv1_2': True,
    'tlsv1_1': True,
    'hide_rejected_ciphers': True,
    'quiet': None, 'keypass': '',
    'cert': None, 'timeout': 5,
    'xmpp_to': None
}





