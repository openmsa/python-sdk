"""
This module provides the Profile class for interacting with profiles in the MSA SDK.

The Profile class inherits from MSA_API and provides methods to check the existence
of profiles and perform other profile-related operations.
"""

import json

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
        self.path = '{}/ref?extRef={}'.format(self.api_path, reference)
        self._call_get()
        return self.response is not None and getattr(self.response, "status_code", None) == 200