"""Package SDK."""
__version__ = "2.1.89"
VERSION = "2.1.89"

import base64
import datetime
import logging
import os
import socket
import sys

import msa_sdk.constants as constants
from msa_sdk.variables import Variables

context = Variables.load_context()

def addFileHandler(logger):
    """Add default file handler."""
    if ('service_id' in context):
        service_id = context['service_id']
        process_id = context['PROCESSINSTANCEID'] if 'PROCESSINSTANCEID' in context else ""
        traceId = context['TRACEID'] if "TRACEID" in context else ""
        spanId = context['SPANID'] if "SPANID" in context else ""
        # Create process log handler
        process_log_path = '{}/process-{}.log'.format(constants.PROCESS_LOGS_DIRECTORY, service_id)
        fh = logging.FileHandler(process_log_path)
        formatter = logging.Formatter('%(asctime)s|' + process_id +'|' + VERSION + '|' + traceId + '|' + spanId + '|%(module)s|' + socket.gethostname() + '|%(levelname)s\n%(message)s\n')
        logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

# ES index
def addEsHandler(logger):
    """ES log handler."""
    if ('ES_SERVERS' in os.environ):
        esServer = os.environ['ES_SERVERS']
        auth_details = None
        if('ES_CREDENTIALS' in os.environ):
            auth = os.environ['ES_CREDENTIALS']
            arr = base64.b64decode(auth).decode()
            res = arr.split(":", 1)
            auth_details = (res[0], res[1])
        esh = EsHandler(auth_details=auth_details, hosts=esServer, raise_on_indexing_exceptions=True, context=context)
        logger.addHandler(esh)

def addStdErr(logger):
    """Add stdErr handler."""
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    #logger.addHandler(handler)

logger = logging.getLogger()
addFileHandler(logger)
addStdErr(logger)

if ('_DEBUG' in os.environ or '_DEBUG' in context):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

#
# Remove elasticsearch query from user logs.
#
logger2 = logging.getLogger('elasticsearch')
logger2.setLevel(logging.ERROR)
logger2 = logging.getLogger('urllib3')
logger2.setLevel(logging.INFO)
logger2 = logging.getLogger('urllib3.connectionpool')
logger2.setLevel(logging.INFO)

