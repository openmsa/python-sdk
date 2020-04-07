"""Module lookup."""

from msa_sdk.msa_api import MSA_API


class Customer(MSA_API):
    """Class Customer."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path = "/customer"

    def create_customer_by_prefix(self, prefix, name="", reference=""):
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
        self.path = "{}/{}?name={}&reference={}".format(self.api_path, prefix,
                                                        name, reference)
        params = {}
        self.call_post(params)

    def get_customer_by_id(self, id):
        """

        Get customer by id.

        Parameters
        -----------
        id: Integer
                MSA ID for customer

        Returns
        -------
        JSON with customer information

        """
        self.action = "Get customer by ID"
        self.path = "{}/id/{}".format(self.api_path, id)
        self.call_get()
        return self.content

    def update_customer_by_id(self, id, name=""):
        """

        Update customer by id.

        Parameters
        -----------
        id: Integer
                MSA ID for customer

        Returns
        -------
        JSON with customer information

        """
        self.action = "Update customer by ID"
        self.path = '{}/id/{}'.format(self.api_path, id)
        params = {
            "name": name
        }
        self.call_put(params)

    def delete_customer_by_id(self, id):
        """

        Delete customer by id.

        Parameters
        -----------
        id: Integer
                MSA ID for customer

        Returns
        -------
        None

        """
        self.action = 'Delete customer by ID'
        self.path = '{}/id/{}'.format(self.api_path, id)
        self.call_delete()

    def update_variables_by_reference(self, reference, name="", value=""):
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
        self.path = '{}/reference/{}/variables'.format(
            self.api_path, reference)
        params = {
            "name": name,
            "value": value
        }
        self.call_put(params)

    def attach_profile_by_reference(self, reference, profile=""):
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
        self.path = '{}/{}/attach'.format(self.api_path, reference)
        params = {
            "profile": profile
        }
        self.call_put(params)

    def detach_profile_by_reference(self, reference, profile=""):
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
        self.path = '{}/{}/detach'.format(self.api_path, reference)
        params = {
            "profile": profile
        }
        self.call_put(params)

    def get_variables_by_id(self, id):
        """

        Get configuration variables by customer ID.

        Parameters
        -----------
        ID: Integer
                Customer ID

        Returns
        -------
        JSON body of configuration variables

        """
        self.action = 'Get configuration variables by ID'
        self.path = '{}/id/{}/variables'.format(self.api_path, id)
        self.call_get()
        return self.content

    def get_variables_by_name(self, id, name):
        """

        Get configuration variable info by variable name.

        Parameters
        -----------
        ID: Integer
                Customer ID
        Name: String
                Variables name

        Returns
        -------
        JSON body of variable info

        """
        self.action = 'Get configuration variable info by variable name'
        self.path = '{}/id/{}/variables/{}'.format(self.api_path, id, name)
        self.call_get()
        return self.content

    def get_customer_by_reference(self, reference):
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
        self.path = "{}/reference/{}".format(self.api_path, reference)
        self.call_get()
        return self.content

    def delete_customer_by_reference(self, reference):
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
        self.path = "{}/reference/{}".format(self.api_path, reference)
        self.call_delete()

    def delete_variable_by_name(self, id, name):
        """

        Delete configuration variable info by variable name.

        Parameters
        -----------
        ID: Integer
                Customer ID
        Name: String
                Variables name

        Returns
        -------
        None

        """
        self.action = 'Delete configuration variable info by variable name'
        self.path = '{}/id/{}/variables/{}'.format(self.api_path, id, name)
        self.call_delete()
