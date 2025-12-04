"""Module customer (subtenant)."""

import json

from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device


class Customer(MSA_API):
    """Class Customer."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path = "/customer"

    def get_device_list_by_id(self, customer_id: int) -> list:
        """

        Get device list for the customer.

        Parameters
        -------
        id: Integer
            MSA ID for customer (subtenant)

        Returns
        -------
        return_list: list()
                     List of device Id of the customer (subtenant)

        """
        return_list = []

        self.path = f"/device/v1/customer/{customer_id}/device-features"
        self._call_get()

        for device in json.loads(self.content):
            return_list.append(device['id'])

        return return_list

    def get_ip_address_list(self, customer_id: int) -> list:
        """

        Get device ip address list for the customer (subtenant).

        Parameters
        -------
        id: Integer
            MSA ID for customer (subtenant)

        Returns
        -------
        return_list: list()
                     List of device Id of the customer (subtenant)

        """
        ip_address_list = []
        devices = self.get_device_list_by_id(customer_id)
        for device_id in devices:
            device = Device(device_id=device_id)
            device.read()
            ip_address_list.append(device.management_address)

        return ip_address_list

    def create_customer_by_prefix(self, prefix: str, name="",
                                  reference="") -> None:
        """

        Create customer by prefix.

        Parameters
        -------
        prefix: String
                Unique MSA assigned customer ID
        name: String (Optional)
                Name of customer
        reference: String (Optional)
                MSA reference of customer
        Returns
        -------
        None

        """
        self.action = 'Create customer by prefix'
        path = f"{self.api_path}/{prefix}?name={name}&reference={reference}"
        self.path = path
        self._call_post({})

    def get_customer_by_id(self, customer_id: int) -> str:
        """

        Get customer by id.

        Parameters
        -----------
        customer_id: Integer
                MSA ID for customer

        Returns
        -------
        JSON with customer information

        """
        self.action = "Get customer by ID"
        self.path = "{}/id/{}".format(self.api_path, customer_id)
        self._call_get()
        return self.content

    def update_customer_by_id(self, customer_id: int, name="") -> None:
        """

        Update customer by id.

        Parameters
        -----------
        customer_id: Integer
                MSA ID for customer

        Returns
        -------
        JSON with customer information

        """
        self.action = "Update customer by ID"
        self.path = '{}/id/{}'.format(self.api_path, customer_id)
        params = {
            "name": name
        }
        self._call_put(params)

    def delete_customer_by_id(self, customer_id: int) -> None:
        """

        Delete customer by id.

        Parameters
        -----------
        customer_id: Integer
                MSA ID for customer

        Returns
        -------
        None

        """
        self.action = 'Delete customer by ID'
        self.path = '{}/id/{}'.format(self.api_path, customer_id)
        self._call_delete()

    def update_variables_by_reference(self, reference, name="",
                                      value="") -> None:
        """

        Update variables by reference.

        Parameters
        -----------
        Reference: String
                Customer reference
        Name: String
                Variable name
        Value: String
                Variable value

        Returns
        -------
        JSON body for variables

        """
        self.action = 'Update variables by reference'
        self.path = f'{self.api_path}/reference/{reference}/variables'
        params = {
            "name": name,
            "value": value
        }
        self._call_put(params)

    def attach_profile_by_reference(self, reference: str, profile="") -> None:
        """

        Attach profile to customer by external reference.

        Parameters
        -----------
        Reference: String
                Customer reference
        Profile: String
                Profile

        Returns
        -------
        None

        """
        self.action = 'Attach profile by reference'
        self.path = f'{self.api_path}/{reference}/attach'
        params = {
            "profile": profile
        }
        self._call_put(params)

    def detach_profile_by_reference(self, reference: str, profile="") -> None:
        """

        Detach profile to customer by external reference.

        Parameters
        -----------
        Reference: String
                Customer reference
        Profile: String
                Profile

        Returns
        -------
        None

        """
        self.action = 'Detach profile by reference'
        self.path = f'{self.api_path}/{reference}/detach'
        params = {
            "profile": profile
        }
        self._call_put(params)

    def get_variables_by_id(self, customer_id: int) -> str:
        """

        Get configuration variables by customer ID.

        Parameters
        -----------
        customer_id: Integer
                Customer ID

        Returns
        -------
        JSON body of configuration variables

        """
        self.action = 'Get configuration variables by ID'
        self.path = f'{self.api_path}/id/{customer_id}/variables'
        self._call_get()
        return self.content

    def get_variables_by_name(self, customer_id: int, name: str) -> str:
        """

        Get configuration variable info by variable name.

        Parameters
        -----------
        customer_id: Integer
                Customer ID
        Name: String
                Variables name

        Returns
        -------
        JSON body of variable info

        """
        self.action = 'Get configuration variable info by variable name'
        self.path = f'{self.api_path}/id/{customer_id}/variables/{name}'
        self._call_get()
        return self.content

    def get_customer_by_reference(self, reference: str) -> str:
        """

        Get customer by reference.

        Parameters
        -----------
        Reference: String
                External reference for customer

        Returns
        -------
        JSON with customer information

        """
        self.action = "Get customer by reference"
        self.path = f"{self.api_path}/reference/{reference}"
        self._call_get()
        return self.content

    def delete_customer_by_reference(self, reference: str) -> None:
        """

        Delete customer by reference.

        Parameters
        -----------
        Reference: String
                External reference for customer

        Returns
        -------
        None

        """
        self.action = "Delete customer by reference"
        self.path = f"{self.api_path}/reference/{reference}"
        self._call_delete()

    def delete_variable_by_name(self, customer_id: int, name: str) -> None:
        """

        Delete configuration variable info by variable name.

        Parameters
        -----------
        customer_id: Integer
                Customer ID
        name: String
                Variables name

        Returns
        -------
        None

        """
        self.action = 'Delete configuration variable info by variable name'
        self.path = f'{self.api_path}/id/{customer_id}/variables/{name}'
        self._call_delete()

    def get_deployment_settings_by_customer_id(self, customer_id: int) -> str:
        """
        Get list of deployment settings and their attributes.

        Parameters
        ----------
        cusotmer_id: integer
            Customer ID
        Returns
        -------
            Json:
                  Deployment settings list for the customer

        """
        self.action = ("Get deploymnet settings profile "
                       "attached to the customer")
        self.path = f"/conf-profile/v2/list/customer/{customer_id}"
        self._call_get()
        return json.loads(self.content)
