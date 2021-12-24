"""Module msa_api."""
import datetime
import json
import os
import re
import sys
from pathlib import Path

import requests

from msa_sdk import constants
from msa_sdk.variables import Variables


def host_port():
    """
    Hostname and port of the API.

    Returns
    -------
    Hostname and Port

    """
    return('localhost', '8480')


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

        self._token = Variables.task_call()['TOKEN']
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
        def log_to_file(log_id, log_msg, process_id):
            """

            Log a message to a log file with corresponding to a process id.

            Parameters
            ---------
            log_id: Integer
                Log file id

            log_msg: String
                Message to be logged

            process_id: String
                Process Id

            Returns
            ------
            Json

            """
            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_file = '{}/process-{}.log'.format(
                constants.PROCESS_LOGS_DIRECTORY,
                log_id)
            with open(log_file, 'a+') as f_log:
                f_log.write('\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
                    log_time, process_id, log_msg, log_time, process_id))

        response = {
            "wo_status": status,
            "wo_comment": comment,
            "wo_newparams": new_params
        }

        json_response = json.dumps(response)

        if log_response:
            pretty_json = json.dumps(new_params, indent=4)
            log_to_file(
                new_params['SERVICEINSTANCEID'],
                pretty_json,
                new_params['PROCESSINSTANCEID'])

        return json_response

    @classmethod
    def task_error(cls, comment, context, log_response=True):
        """

        Task error and print.

        Parameters
        ----------
        comment: String
            Comment
        new_params: Dictionary
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
        new_params: Dictionary
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
        return self._token

    @property
    def content(self):
        """Content of the response."""
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
            'Authorization': 'Bearer {}'.format(self._token),
        }
        if data is None:
            data = {}

        if isinstance(data, dict):
            data = json.dumps(data)
        else:
            raise TypeError('Parameters needs to be a dictionary')

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
            'Authorization': 'Bearer {}'.format(self._token),
        }

        url = self.url + self.path
        self.response = requests.get(url, headers=headers, timeout=timeout,
                                     params=params)
        self._content = self.response.text
        self.check_response()

    def _call_put(self, data=None):
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
            'Authorization': 'Bearer {}'.format(self._token),
        }
        url = self.url + self.path
        self.response = requests.put(url, data=data, headers=headers)
        self._content = self.response.text
        self.check_response()

    def _call_delete(self):
        """
        Call -XDELETE. This is a private method.

        This method that should not be used outside this sdk scope.

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
        self._content = self.response.text
        self.check_response()

    def log_to_process_file(self, processId: str, log_message: str) -> bool:
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
        import sys
        process_log_path = '{}/process-{}.log'.format(
            constants.PROCESS_LOGS_DIRECTORY, processId)
        current_time = datetime.datetime.now().isoformat()
        log_string = '{date}:{file}:DEBUG:{msg}\n'.format(
            date=current_time, file=sys.argv[0].split('/')[-1],
            msg=log_message)
        try:
            with open(process_log_path, 'a') as log_file:
                log_file.write(log_string)
                return True
        except IOError:
            return False
