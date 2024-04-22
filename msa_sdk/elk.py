"""Elastic search loggin module."""
import datetime
import logging
import socket
import sys
from enum import Enum
from threading import Lock
from threading import Timer

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from elasticsearch import helpers as eshelpers
from elasticsearch.serializer import JSONSerializer


# Have a look at https://github.com/cmanaha/python-elasticsearch-logger
class EsSerializer(JSONSerializer):
    """
    JSON serializer inherited from the elastic search JSON serializer.

    Allows to serialize logs for a elasticsearch use.
    Manage the record.exc_info containing an exception type.
    """

    def default(self, data):
        """
        Override the elasticsearch default method.

        Allows to transform unknown types into strings.

        :params data: The data to serialize before sending it to elastic search
        """
        try:
            return super(EsSerializer, self).default(data)
        except TypeError:
            return str(data)

class EsHandler(logging.Handler):
    """Elastic search handler."""

    class IndexNameFrequency(Enum):
        """
        Index type supported the handler supports.

        - Daily indices
        - Weekly indices
        - Monthly indices
        - Year indices
        """

        DAILY = 0
        WEEKLY = 1
        MONTHLY = 2
        YEARLY = 3

    __LOGGING_FILTER_FIELDS = ['msecs',
                               'relativeCreated',
                               'levelno',
                               'created']
    @staticmethod
    def _get_daily_index_name(es_index_name):
        """
        Return elasticearch index name.

        :param: index_name the prefix to be used in the index
        :return: A srting containing the elasticsearch indexname used which should include the date.
        """
        return "{0!s}-{1!s}".format(es_index_name, datetime.datetime.now().strftime('%Y.%m.%d'))
    
    __DEFAULT_ELASTICSEARCH_HOST = [{'host': 'msa-es', 'port': 9200}]
    __DEFAULT_AUTH_USER = 'superuser'
    __DEFAULT_AUTH_PASSWD = ''
    __DEFAULT_INDEX_FREQUENCY = IndexNameFrequency.DAILY
    __DEFAULT_BUFFER_SIZE = 1000
    __DEFAULT_FLUSH_FREQ_INSEC = 1
    __DEFAULT_ADDITIONAL_FIELDS = {}
    __DEFAULT_ES_INDEX_NAME = 'process-log'
    __DEFAULT_ES_DOC_TYPE = 'process-log'
    __DEFAULT_RAISE_ON_EXCEPTION = False
    __DEFAULT_TIMESTAMP_FIELD_NAME = "timestamp"

    def __init__(self,
                  hosts=__DEFAULT_ELASTICSEARCH_HOST,
                  auth_details=(__DEFAULT_AUTH_USER, __DEFAULT_AUTH_PASSWD),
                  buffer_size=__DEFAULT_BUFFER_SIZE,
                  flush_frequency_in_sec=__DEFAULT_FLUSH_FREQ_INSEC,
                  es_index_name=__DEFAULT_ES_INDEX_NAME,
                  index_name_frequency=__DEFAULT_INDEX_FREQUENCY,
                 es_doc_type=__DEFAULT_ES_DOC_TYPE,
                 es_additional_fields=__DEFAULT_ADDITIONAL_FIELDS,
                 raise_on_indexing_exceptions=__DEFAULT_RAISE_ON_EXCEPTION,
                 default_timestamp_field_name=__DEFAULT_TIMESTAMP_FIELD_NAME,
                 context= {}):
        """
        Initialize a constructor.
        
        A constructor.
        """
        logging.Handler.__init__(self)
        self.context = context
        self.hosts = hosts
        self.auth_details = auth_details
        self.buffer_size = buffer_size
        self.flush_frequency_in_sec = flush_frequency_in_sec
        self.es_index_name = es_index_name
        self.index_name_frequency = index_name_frequency
        self.es_doc_type = es_doc_type
        self.es_additional_fields = es_additional_fields.copy()
        self.es_additional_fields.update({'host': socket.gethostname(),
                                         'host_ip': socket.gethostbyname(socket.gethostname()),
                                         'service_id': context['SERVICEINSTANCEID'] if "SERVICEINSTANCEID" in context else "",
                                         'process_id': context['PROCESSINSTANCEID'] if "PROCESSINSTANCEID" in context else "empty",
                                         'trace_id': context['TRACEID'] if "TRACEID" in context else "",
                                         'span_id': context['SPANID'] if "SPANID" in context else "",
                                         'task_id': sys.argv[0]
                                         })
        self.raise_on_indexing_exceptions = raise_on_indexing_exceptions
        self.default_timestamp_field_name = default_timestamp_field_name
        self.serializer = EsSerializer()
        self._client = None
        self._buffer = []
        self._buffer_lock = Lock()
        self._index_name_func = EsHandler._get_daily_index_name
        self._timer = None

    def __schedule_flush(self):
        if self._timer is None:
            self._timer = Timer(self.flush_frequency_in_sec, self.flush)
            self._timer.setDaemon(True)
            self._timer.start()

    def __get_es_client(self):
         return Elasticsearch(hosts=self.hosts,
                                     http_auth=self.auth_details,
                                     use_ssl=False,
                                     verify_certs=False,
                                     connection_class=RequestsHttpConnection,
                                     serializer=self.serializer)
    def test_es_source(self):
        """
        Returns True if the handler can ping the Elasticsearch servers.

        Can be used to confirm the setup of a handler has been properly done and confirm
        that things like the authentication is working properly.

        :return: A boolean, True if the connection against elasticserach host was successful
        """
        return self.__get_es_client().ping()

    @staticmethod
    def __get_es_datetime_str(timestamp):
        """
        Return elasticsearch utc formatted time for an epoch timestamp.

        :param timestamp: epoch, including milliseconds
        :return: A string valid for elasticsearch time record
        """
        current_date = datetime.datetime.utcfromtimestamp(timestamp)
        return "{0!s}.{1:03d}Z".format(current_date.strftime('%Y-%m-%dT%H:%M:%S'), int(current_date.microsecond / 1000))
    
    def flush(self):
        """
        Flushes the buffer into ES.

        :return: None
        """
        if self._timer is not None and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None

        if self._buffer:
            try:
                with self._buffer_lock:
                    logs_buffer = self._buffer
                    self._buffer = []
                actions = (
                    {
                        '_index': self._index_name_func(self.es_index_name),
                        '_source': log_record
                    }
                    for log_record in logs_buffer
                )
                eshelpers.bulk(
                    client=self.__get_es_client(),
                    actions=actions,
                    stats_only=True
                )
            except Exception as exception:
                if self.raise_on_indexing_exceptions:
                    # Do nothing.
                    return
    def close(self):
        """
        Flushes the buffer and release any outstanding resource.

        :return: None
        """
        if self._timer is not None:
            self.flush()
        self._timer = None

    def emit(self, record):
        """
        Emit overrides the abstract logging.Handler logRecord emit method.

        Format and records the log

        :param record: A class of type ```logging.LogRecord```
        :return: None
        """
        self.format(record)

        rec = self.es_additional_fields.copy()
        for key, value in record.__dict__.items():
            if key not in EsHandler.__LOGGING_FILTER_FIELDS:
                if key == "args":
                    value = tuple(str(arg) for arg in value)
                rec[key] = "" if value is None else value
        rec[self.default_timestamp_field_name] = self.__get_es_datetime_str(record.created)
        with self._buffer_lock:
            self._buffer.append(rec)

        if len(self._buffer) >= self.buffer_size:
            self.flush()
        else:
            self.__schedule_flush()