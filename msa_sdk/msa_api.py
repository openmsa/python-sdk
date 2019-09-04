"""Module msa_api."""
import datetime
import json
import re

import requests

from msa_sdk import constants


def host_port():
    """
    Hostname and port of the API.

    Returns
    -------
    Hostname and Port

    """
    api_info = open(constants.VARS_CTX_FILE).read()

    widlfly_address = re.search(r'UBI_WILDFLY_JNDI_ADDRESS=(.+)',
                                api_info).group(1)
    widlfly_port = re.search(r'UBI_WILDFLY_JNDI_PORT=(\d+)',
                             api_info).group(1)

    return (widlfly_address, widlfly_port)


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
        self._token = self._get_token()
        self.path = None
        self.response = None
        self.log_response = True
        self._content = None
        self.action = self.__class__

    @classmethod
    def process_content(cls, status, comment, new_params, log_response=False):
        """

        Process content.

        Parameters
        ----------
        status: String
            Status ID: 'ENDED', 'FAIL', 'RUNNING', 'WARNING', PAUSE
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
        def log_to_file(log_id, log_msg):
            """

            Log a message to a log file with corresponding to a process id.

            Parameters
            ---------
            log_id: Integer
                Log file id

            log_msg: String
                Message to be logged

            Returns
            ------
            Json

            """
            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_file = '{}/process-{}.log'.format(
                constants.PROCESS_LOGS_DIRECTORY,
                log_id)
            with open(log_file, 'a+') as f_log:
                f_log.write('\n=== {} ===\n{}'.format(log_time, log_msg))

        response = {
            "wo_status": status,
            "wo_comment": comment,
            "wo_newparams": new_params
        }

        json_response = json.dumps(response)

        if log_response:
            pretty_json = json.dumps(new_params, indent=4)
            log_to_file(new_params['SERVICEINSTANCEID'], pretty_json)

        return json_response

    @property
    def token(self):
        """
        Property API Token.

        Returns
        -------
        Token

        """
        return self._token

    @property
    def content(self):
        """Content of the response."""
        return self._content

    def _get_token(self):
        headers = {'Content-Type': 'application/json'}
        data = '{"username":"ncroot", "password":"ubiqube"}'
        url = self.url + '/auth/token'
        response = requests.post(url, headers=headers, data=data).json()
        return response['token']

    def check_response(self):
        """
        Check reponse of a POST/GET/PUT/DELETE.

        Returns
        --------
        None


        """
        if not self.response.ok:
            self._content = self.process_content(self.FAILED, self.action,
                                                 self.response.reason)

    def call_post(self, data=None, timeout=60):
        """
        Call -XPOST.

        Returns
        --------
        None

        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._token),
        }

        if not data:
            data = json.dumps(data)

        url = self.url + self.path
        self.response = requests.post(url, headers=headers, data=data,
                                      timeout=timeout)
        self._content = self.response.content
        self.check_response()

    def call_get(self, timeout=60):
        """
        Call -XGET.

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._token),
        }

        url = self.url + self.path
        self.response = requests.get(url, headers=headers, timeout=timeout)
        self._content = self.response.content
        self.check_response()

    def call_put(self, data=None):
        """
        Call -XPUT.

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
            'Authorization': 'Bearer {}'.format(self._token),
        }
        url = self.url + self.path
        self.response = requests.put(url, data=data, headers=headers)
        self._content = self.response.content
        self.check_response()

    def call_delete(self):
        """
        Call -XDELETE.

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._token),
        }
        url = self.url + self.path
        self.response = requests.delete(url, headers=headers)
        self._content = self.response.content
        self.check_response()
