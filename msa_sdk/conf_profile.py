"""Module ConfProfile."""
import json

from msa_sdk.msa_api import MSA_API


class ConfProfile(MSA_API):
    """Class ConfProfile."""

    def __init__(self, profile_id=None, name=None, externalReference=None,
                 comment=None, vendor_id=None, model_id=None,
                 microserviceUris=[], templateUris=[],
                 attachedManagedEntities=[], customer_id=None):
        """
        Initialize.

        Parameters
        ----------
        profile_id: Integer
                Profile id
        name: String
                Profile Name
        externalReference: String
                Configurable id for Profile
        comment: String
                Configurable id for Profile
        vendor_id: Integer
                Manufacture ID
        model_id: Integer
                Model ID
        login: String
                Login
        microserviceUris: List
                List of Microservices you want to attach
        templateUris: List
                List of Templates you want to attach
        attachedManagedEntities: List
                List of Managed Entities you want to attach
        customer_id: Integer
                Customer id which you want to attach a created
                    configuration profile

        Returns
        -------
        None

        """
        MSA_API.__init__(self)
        self.api_path = "/conf-profile"
        self.profile_id = profile_id
        self.name = name
        self.externalReference = externalReference
        self.comment = comment
        self.vendor_id = vendor_id
        self.model_id = model_id
        self.microserviceUris = microserviceUris
        self.templateUris = templateUris
        self.attachedManagedEntities = attachedManagedEntities
        self.customer_id = customer_id

        if profile_id:
            self.read()

    def create(self):
        """

        Create configuration profile.

        Returns
        -------
        None

        """
        self.action = 'Create configuration profile'
        self.path = "{}/v2/{}".format(self.api_path, self.customer_id)
        params = {
            "id": self.profile_id,
            "name": self.name,
            "externalReference": self.externalReference,
            "comment": self.comment,
            "model": {
                "id": self.model_id
            },
            "vendor": {
                "id": self.vendor_id
            },
            "microserviceUris": self.microserviceUris,
            "templateUris": self.templateUris,
            "attachedManagedEntities": self.attachedManagedEntities
        }
        self.call_post(params)

    def read(self):
        """

        Get configuration profile by id.

        Returns
        -------
        JSON with configuration profile information

        """
        self.action = "Get configuration profile by ID"
        self.path = "{}/v2/{}".format(self.api_path, self.profile_id)
        self.call_get()

        conf_profile = json.loads(self.content)

        self.profile_id = conf_profile['id']
        self.name = conf_profile['name']
        self.externalReference = conf_profile['externalReference']
        self.comment = conf_profile['comment']
        self.model_id = conf_profile['model']['id']
        self.vendor_id = conf_profile['vendor']['id']
        microserviceUris = conf_profile['microserviceUris']
        self.microserviceUris = list(
            microserviceUris.keys()) if microserviceUris else []
        self.templateUris = conf_profile['templateUris']
        self.attachedManagedEntities = conf_profile['attachedManagedEntities']
        self.customer_id = conf_profile['customerIds'][0]

        return self.content

    def update(self):
        """

        Update configuration profile by id.

        Returns
        -------
        JSON with configuration profile information

        """
        self.action = "Update configuration profile by ID"
        self.path = "{}/v2/{}?customer_id={}".format(
            self.api_path, self.profile_id, self.customer_id)
        data = {
            "name": self.name,
            "externalReference": self.externalReference,
            "comment": self.comment,
            "model": {
                "id": self.model_id
            },
            "vendor": {
                "id": self.vendor_id
            },
            "microserviceUris": self.microserviceUris,
            "templateUris": self.templateUris,
            "attachedManagedEntities": self.attachedManagedEntities
        }
        self.call_put(json.dumps(data))

        return self.content

    def delete(self):
        """

        Delete configuration profile by id.

        Returns
        -------
        None

        """
        self.action = 'Delete configuration profile by ID'
        self.path = '{}/v2/{}'.format(self.api_path, self.profile_id)
        self.call_delete()
