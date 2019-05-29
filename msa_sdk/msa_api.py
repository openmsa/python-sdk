"""Module msa_api."""
import requests


def host_port():
    """
    Hostname and port of the API.

    Returns
    -------
    Hostname and Port

    """
    return ('10.30.18.86', '80')


class MSA_API():  # pylint: disable=invalid-name
    """Class MSA API."""

    def __init__(self):
        """Initialize."""
        self.url = 'http://{}:{}/ubi-api-rest'.format(*host_port())
        self._token = self._get_token()
        self.path = None
        self.response = None

    @property
    def token(self):
        """
        Property API Token.

        Returns
        -------
        None

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
