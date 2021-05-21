"""Module lookup."""

from msa_sdk.msa_api import MSA_API


class Lookup(MSA_API):
    """Class Lookup."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path_v1 = "/lookup/v1"
        self.api_path = "/lookup"

    def look_list_device_ids(self):
        """Look list devices ids.

        Returns
        -------
        None

        """
        self.action = 'Get device ids'
        self.path = '{}/devices'.format(self.api_path)
        self._call_get()

    def look_list_customer_ids(self):
        """Look list customer ids.

        Returns
        -------
        None

        """
        self.action = 'Get customer ids'
        self.path = '{}/customers'.format(self.api_path)
        self._call_get()

    def look_list_manager_ids(self):
        """Look list manager ids.

        Returns
        -------
        None

        """
        self.action = 'Get manager ids'
        self.path = '{}/managers'.format(self.api_path)
        self._call_get()

    def look_list_operators_id(self, manager_id):
        """Look list operators id.

        Parameters
        ----------
        manager_id: Integer
            Manager id

        Returns
        -------
        None

        """
        self.action = 'Get operators id'
        self.path = '{}/operators/id/{}'.format(self.api_path, manager_id)
        self._call_get()

    def look_list_sec_nodes(self):
        """Look list sec nodes.

        Returns
        -------
        None

        """
        self.action = 'Get sec nodes'
        self.path = '{}/sec_nodes'.format(self.api_path)
        self._call_get()

    def look_list_device_by_customer_ref(self, custom_ref):
        """Look list device by customer reference.

        Parameters
        ----------
        manager_id: Integer
            Manager id

        Returns
        -------
        None

        """
        self.action = 'Get list device by customer reference'
        self.path = '{}/customer/devices/reference/{}'.format(self.api_path,
                                                              custom_ref)
        self._call_get()
