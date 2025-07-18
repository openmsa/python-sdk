"""Module geolocation."""

import json

from msa_sdk.msa_api import MSA_API


class Geolocation(MSA_API):
    """Class Geolocation."""

    def __init__(self, site_id=None):
        """
        Initialize.

        Parameters
        ----------
        site_id: String
                 Site id

        Returns
        -------
        None
        """
        MSA_API.__init__(self)
        self.site_id = site_id
        self.api_path = "/device/v1/site"
        
    def get_geolocation(self) -> dict:
        """
        Get the geolocation (latitude, longitude) of a ME.

        Parameters
        ----------
        None

        Returns
        -------
        latitude, longitude: Dict()

        """
        self.action = 'Get the geolocation'
        self.path = f'{self.api_path}/{self.site_id}/geo-localization'
        self._call_get()

        return json.loads(self.content)

    def set_geolocation(self, latitude: str, longitude: str):
        """
        Set the geolocation (latitude, longitude) of a ME.

        Parameters
        ----------
        latitude: String
                  Modified latitude 
        
        longitude: String
                  Modified longitude

        Returns
        -------
        None

        """
        self.action = 'Set the geolocation'
        self.path = f'{self.api_path}/geo-localization?siteId={self.site_id}&latitude={latitude}&longitude={longitude}'
        self._call_put()
