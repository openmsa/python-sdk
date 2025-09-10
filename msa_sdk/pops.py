"""Module Pops."""

from msa_sdk.msa_api import MSA_API


class Pops(MSA_API):
    """Class Pops."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path = "/sase/pops"

    def save_pops(self, data):
        """
        Save all pops.

        Parameters
        ----------
        data: pops data in json

        Returns
        -------
        None

        """
        self.action = 'Save Pops'
        self.path = '{}'.format(self.api_path)
        self._call_post(data)

    def remove_pop(self, pop_type, vendor, name):
        """
        Remove a pop.

        Parameters
        ----------
        pop_type: type of pop
        vendor: vendor of pop
        name: name of pop

        Returns
        -------
        None

        """
        self.action = 'Remove Pop'
        self.path = '{}?popType={}&vendor={}&name={}'.format(self.api_path, pop_type, vendor, name)
        self._call_delete()