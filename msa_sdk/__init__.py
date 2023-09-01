"""Package SDK."""
__version__ = "2.1.88"
VERSION = "2.1.88"

import base64
import logging
import os
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
        formatter = logging.Formatter('%(asctime)s|' + process_id +'|' + VERSION + '|' + traceId + '|' + spanId + '|%(module)s\n%(message)s\n')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

def addStdErr(logger):
    """Add stdErr handler."""
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    #logger.addHandler(handler)

logger = logging.getLogger()
addFileHandler(logger)
addStdErr(logger)

if ('_DEBUG' in os.environ):
    logger.setLevel(logging.DEBUG)

#
# Remove elasticsearch query from user logs.
#
logger2 = logging.getLogger('elasticsearch')
logger2.setLevel(logging.ERROR)
logger2 = logging.getLogger('urllib3')
logger2.setLevel(logging.INFO)
logger2 = logging.getLogger('urllib3.connectionpool')
logger2.setLevel(logging.INFO)

