"""
This module provides the Profile class for interacting with profiles in the MSA SDK.

The Profile class inherits from MSA_API and provides methods to check the existence
of profiles and perform other profile-related operations.
"""
from urllib.parse import urlencode

from msa_sdk.msa_api import MSA_API


class Profile(MSA_API):
    """
    A class to represent a profile in the MSA SDK.

    This class provides methods to interact with profiles.
    """

    def __init__(self):
        """
        Initialize a Profile instance.

        Sets up the API path for profile operations.
        """
        MSA_API.__init__(self)
        self.api_path = "/profile"

    def exist(self, reference) -> bool:
        """
        Check if a profile exists by reference.

        Parameters
        ----------
        reference : str
            The reference identifier for the profile.

        Returns
        -------
        bool
            True if the profile exists, False otherwise.
        """
        self.action = 'Check Profile exist by reference'
        url_encoded = urlencode({'extRef': reference})
        self.path = '{}/ref?{}'.format(self.api_path, url_encoded)
        self._call_get()
        if self.response is None:
            raise Exception("No response received from the server.")
        if self.response.status_code == 404:
            return False
        if self.response.status_code == 200:
            return True
        raise Exception("Unexpected response code: {}".format(self.response.status_code))