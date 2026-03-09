"""Module Pops."""
import json

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

    def remove_pop(self, entity_type, vendor, name):
        """
        Remove a pop.

        Parameters
        ----------
        entity_type: type of pop
        vendor: vendor of pop
        name: name of pop

        Returns
        -------
        None

        """
        self.action = 'Remove Pop'
        self.path = '{}?entityType={}&vendor={}&name={}'.format(self.api_path, entity_type, vendor, name)
        self._call_delete()

    def save_tunnel(self, data: dict) -> None:
        """
        Create/Save a tunnel.

        Parameters
        ----------
        data : create tunnel data in json

        Returns
        -------
        None
        """
        self.action = "Save Tunnel"
        self.path = '{}/tunnel'.format(self.api_path)
        self._call_post(data)

    def update_tunnel(self, cpe_device_id: int, pop_vendor: str, pop_identifier: str, data: dict) -> None:
        """
        Update a tunnel identified by (cpeDeviceId, popVendor, popIdentifier).

        Parameters
        ----------
        cpe_device_id : int
        pop_vendor : str
        pop_identifier : str
        data : update tunnel data in json

        Returns
        -------
        None
        """
        self.action = "Update Tunnel"
        self.path = '{}/tunnel?cpeDeviceId={}&popVendor={}&popIdentifier={}'.format(self.api_path, cpe_device_id,
                                                                                     pop_vendor,
                                                                                     pop_identifier)
        self._call_put(json.dumps(data))

    def list_tunnels(self, tenant_prefix: str, location_id=None):
        """
        Get tunnels in GeoJSON for a tenant prefix (and optional location).

        Parameters
        ----------
        tenant_prefix : str
        location_id : int

        Returns
        -------
        dict
            GeoJSON FeatureCollection
        """
        self.action = "List Tunnels"
        if location_id is not None:
            self.path = '{}/tunnels?tenantPrefix={}&locationId={}'.format(
                self.api_path, tenant_prefix, location_id
            )
        else:
            self.path = '{}/tunnels?tenantPrefix={}'.format(self.api_path, tenant_prefix)
        return self._call_get()

    def remove_tunnel(self, cpe_device_id: int, pop_vendor: str, pop_identifier: str) -> None:
        """
        Delete a tunnel identified by (cpeDeviceId, popVendor, popIdentifier).

        Parameters
        ----------
        cpe_device_id : int
        pop_vendor : str
        pop_identifier : str

        Returns
        -------
        None
        """
        self.action = "Remove Tunnel"
        self.path = '{}/tunnel?cpeDeviceId={}&popVendor={}&popIdentifier={}'.format(self.api_path, cpe_device_id,
                                                                                     pop_vendor,
                                                                                     pop_identifier)
        self._call_delete()