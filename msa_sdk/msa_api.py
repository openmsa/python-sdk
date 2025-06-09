"""Module msa_api."""
import json
import logging
import os
import random
import sys

import requests

from msa_sdk import constants
from msa_sdk import context

logger = logging.getLogger("msa-sdk")

def host_port():
    """
    Hostname and port of the API.

    Returns
    -------
    Hostname and Port

    """
    host = os.environ.get('UBIQUBE_MSA_HOST') or 'localhost'
    port = os.environ.get('UBIQUBE_MSA_PORT') or '8480'
    return (host, port)


class MSA_API():  # pylint: disable=invalid-name
    """Class MSA API."""

    ENDED = constants.ENDED
    FAILED = constants.FAILED
    RUNNING = constants.RUNNING
    WARNING = constants.WARNING
    PAUSED = constants.PAUSED

    def __init__(self):
        """Initialize."""
        self.url = 'http://{}:{}/ubi-api-rest'.format(*host_port())
        self.path = ""
        self.response = None
        self.log_response = True
        self._content = ""
        self.action = self.__class__

    @classmethod
    def process_content(cls, status, comment, new_params, log_response=False):
        """

        Process content.

        Parameters
        ----------
        status: String
            Status ID: 'ENDED', 'FAIL', 'RUNNING', 'WARNING', 'PAUSE'
        comment: String
            Comment
        new_params: Dictionary
            Context
        log_response: Bool
            Write log to a file

        Returns
        -------
        Response content formated

        """
        response = {
            "wo_status": status,
            "wo_comment": comment,
            "wo_newparams": new_params
        }
        if log_response:
            import copy
            woToken = copy.deepcopy(new_params)
            if 'TOKEN' in woToken:
                del woToken['TOKEN']
            pretty_json = json.dumps(woToken, indent=4)
            logger.info(pretty_json)

        json_response = json.dumps(response)
        return json_response

    @classmethod
    def task_error(cls, comment, context, log_response=True):
        """

        Task error and print.

        Parameters
        ----------
        comment: String
            Comment
        context: Dictionary
            Context
        log_response: Bool
            Write log to a file

        Returns
        -------
        None

        """
        print(cls.process_content(constants.FAILED, comment, context,
                                  log_response))
        sys.exit(1)

    @classmethod
    def task_success(cls, comment, context, log_response=True):
        """

        Task success and print.

        Parameters
        ----------
        comment: String
            Comment
        context: Dictionary
            Context
        log_response: Bool
            Write log to a file

        Returns
        -------
        None

        """
        print(cls.process_content(constants.ENDED, comment, context,
                                  log_response))
        sys.exit(0)

    @property
    def token(self):
        """
        Property API Token.

        Returns
        -------
        Token

        """
        try:
            url = os.environ.get('API_TOKEN_URL') or "http://msa-auth:8080/auth/realms/msa/protocol/openid-connect/token"
            params = {"client_id": os.environ.get("CLIENT_ID"), "grant_type": "client_credentials", "client_secret" : os.environ.get("CLIENT_SECRET")}
            response = requests.post(url, data=params)
            data = response.json()
            access_token = data["access_token"]
        except Exception:
            return "12345qwert"
        return access_token

    @property
    def content(self):
        """Content of the response."""
        if not self._content:
            return '{}'
        return self._content

    def check_response(self):
        """
        Check reponse of a POST/GET/PUT/DELETE.

        Returns
        --------
        None


        """
        if not self.response.ok:
            json_response = self.response.json()
            self._content = self.process_content(self.FAILED, self.action,
                                                 json_response['message'])

    def _call_post(self, data=None, timeout=60):
        """
        Call -XPOST. This is a private method.

        This method that should not be used outside this sdk scope.

        Returns
        --------
        None

        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        self.add_trace_headers(headers)
        if data is None:
            data = {}

        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        else:
            raise TypeError('Parameters needs to be a dictionary or a list')

        url = self.url + self.path
        self.response = requests.post(url, headers=headers, data=data,
                                      timeout=timeout)
        self._content = self.response.text
        self.check_response()

    def _call_get(self, timeout=60, params={}):
        """
        Call -XGET. This is a private method.

        This method that should not be used outside this sdk scope.

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        self.add_trace_headers(headers)
        url = self.url + self.path
        self.response = requests.get(url, headers=headers, timeout=timeout,
                                     params=params)
        self._content = self.response.text
        self.check_response()

    def _call_put(self, data=None) -> None:
        """
        Call -XPUT. This is a private method.

        This method that should not be used outside this sdk scope.

        Parameters
        ----------
        data: Data to send

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        self.add_trace_headers(headers)
        url = self.url + self.path
        self.response = requests.put(url, data=data, headers=headers)
        self._content = self.response.text
        self.check_response()

    def _call_delete(self) -> None:
        """
        Call -XDELETE. This is a private method.

        This method that should not be used outside this sdk scope.

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        self.add_trace_headers(headers)
        url = self.url + self.path
        self.response = requests.delete(url, headers=headers)
        self._content = self.response.text
        self.check_response()

    def add_trace_headers(self, headers):
        """Add W3C trace headers."""
        if 'TRACEID' not in context:
            t, s = self.create_trace_id()
            context['TRACEID'] = t
            context['SPANID'] = s
            logger.info("Creating traceId: 00-%s-%s-01", t,s)
        # W3C compatible header
        headers['traceparent'] = '00-{}-{}-01'.format(context['TRACEID'], context['SPANID'])
        # Old X-B3, to be removed.
        headers['X-B3-TraceId'] = context['TRACEID']
        headers['X-B3-SpanId'] = context['SPANID']

    def log_to_process_file(self, process_id: str, log_message: str) -> bool:
        """

        Write log string with ISO timestamp to process log file.

        Parameters
        ----------
        process_id: String
                    Process ID of current process
        log_message: String
                     Log text

        Returns
        -------
        True:  log string has been written correctlly
        False: log string has not been written correctlly or the log
            file doesnt exist

        """
        import logging
        logger = logging.getLogger("msa-sdk")
        logger.info(log_message)
        return True

    def create_trace_id(self):
        """Create a new traceId/spanId."""
        trace_id = '%032x' % random.randrange(16**32)
        span_id = '%016x' % random.randrange(6**23)
        return trace_id, span_id
