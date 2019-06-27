"""Module msa_api."""
import requests


def host_port():
    """
    Hostname and port of the API.

    Returns
    -------
    Hostname and Port

    """
    return ('10.30.18.86', '8480')


PROCESS_LOGS_DIRECTORY = '/opt/jboss/latest/logs/processLog'


class MSA_API():  # pylint: disable=invalid-name
    """Class MSA API."""

    def __init__(self):
        """Initialize."""
        self.url = 'http://{}:{}/ubi-api-rest'.format(*host_port())
        self._token = self._get_token()
        self.path = None
        self.response = None

    def content(self, status, comment, new_params, log_response=False):
        """
        Property content

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
            Log a message to a log file with corresponding to a process id
            """

            log_file = '{}/process-{}.log'.format(
                PROCESS_LOGS_DIRECTORY, log_id)
            f_log = open(log_file, 'a+')
            f_log.write(log_msg)
            f_log.close()

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
            print(self.response.reason)
            raise RuntimeError

    def call_post(self):
        """
        Call -XPOST.

        Returns
        --------
        None

        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._token),
        }
        url = self.url + self.path
        self.response = requests.post(url, headers=headers)

    def call_get(self):
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
        self.response = requests.get(url, headers=headers)
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
        self.check_response()
