"""Package SDK."""
__pdoc__ = {
    'elk': False
}
__version__ = "2.2.34"
VERSION = "2.2.34"

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

def add_file_handler(logger):
    """Add default file handler."""
    if ('service_id' in context):
        service_id = context['service_id']
        process_id = context['PROCESSINSTANCEID'] if 'PROCESSINSTANCEID' in context else ""
        trace_id = context['TRACEID'] if "TRACEID" in context else ""
        span_id = context['SPANID'] if "SPANID" in context else ""
        # Create process log handler
        process_log_path = '{}/process-{}.log'.format(constants.PROCESS_LOGS_DIRECTORY, service_id)
        fh = logging.FileHandler(process_log_path)
        formatter = logging.Formatter('%(asctime)s|' + process_id +'|' + VERSION + '|' + trace_id + '|' + span_id + '|%(module)s|' + socket.gethostname() + '|%(levelname)s\n%(message)s\n')
        logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

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
add_file_handler(logger)
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
