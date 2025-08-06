"""Package SDK."""
__pdoc__ = {
    'elk': False
}
__version__ = "2.3.23"
VERSION = "2.3.23"

import base64
import datetime
import logging
import os
import socket
import sys

import msa_sdk.constants as constants
from msa_sdk.elk import EsHandler
from msa_sdk.variables import Variables

context = Variables.load_context()

# ES index
def add_es_handler(logger):
    """ES log handler."""
    if ('ES_SERVERS' in os.environ):
        es_server = os.environ['ES_SERVERS'].split(" ")
        auth_details = None
        if('ES_CREDENTIALS' in os.environ):
            auth = os.environ['ES_CREDENTIALS']
            arr = base64.b64decode(auth).decode()
            res = arr.split(":", 1)
            auth_details = (res[0], res[1])
        esh = EsHandler(auth_details=auth_details, hosts=es_server, raise_on_indexing_exceptions=True, context=context)
        logger.addHandler(esh)

def add_std_err(logger):
    """Add stdErr handler."""
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    #logger.addHandler(handler)

logger = logging.getLogger()
add_std_err(logger)
add_es_handler(logger)

if ('_DEBUG' in os.environ or '_DEBUG' in context):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

#
# Remove elasticsearch query from user logs.
#
logger2 = logging.getLogger('opensearch')
logger2.setLevel(logging.ERROR)
logger2 = logging.getLogger('urllib3')
logger2.setLevel(logging.INFO)
logger2 = logging.getLogger('urllib3.connectionpool')
logger2.setLevel(logging.INFO)
