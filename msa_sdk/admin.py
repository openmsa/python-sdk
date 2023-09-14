"""Module Admin."""
import json

from msa_sdk.msa_api import MSA_API


class Admin(MSA_API):
    """Class Admin."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path_v1 = "/system-admin/v1"
        self.api_path = "/system-admin"
        self.api_path_v2 = "/system-admin/v2"

    def get_vars_value(self, variable_name):
        """
        Get vars value.

        Parameters
        ----------
        variable_name: String
            Variables name

        Returns
        -------
        string: Variable Value

        """
        self.action = 'Get Variable Value'
        self.path = '{}/msa_vars?name={}'.format(self.api_path_v1,
                                                 variable_name)
        self._call_get()
        result = json.loads(self.content)
        return result[0]['value']
