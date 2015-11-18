__author__ = '32hoda1bif'


HOST_QUEUE_TIMEOUT = 30

NUMBER_PROCESSES = 1

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 50001
SERVER_AUTH = b'abc'



COMMAND_LIST = [
    # "reneg",
    "tlsv1_2",
    # "compression",
    # "certinfo",
    "tlsv1_1",
    # "hsts",
    # "resum",
    # "resum_rate",
    # "heartbleed",
    # "chrome_sha1",
    "sslv3",
    "sslv2",
    "tlsv1",
]

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





