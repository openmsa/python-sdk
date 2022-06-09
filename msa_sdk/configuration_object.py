"""Module Configuration Object."""

from msa_sdk.msa_api import MSA_API


class ConfigurationObject(MSA_API):
    """Class Configuration Ojbect."""

    def __init__(self):
        """
        Initialize.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        MSA_API.__init__(self)
        self.api_path = "/configuration-objects"

    def delete(self, device_id: int, object_name: str = "") -> None:
        """
        Delete microservice object instance.

        Parameters
        ----------
        device_id: Integer
                Device id

        object_name: String
                Object name

        Returns
        -------
        None
        """
        if object_name:
            self.path = "{}/{}/{}".format(self.api_path, device_id,
                                          object_name)
        else:
            self.path = "{}/{}".format(self.api_path, device_id)

        self._call_delete()
