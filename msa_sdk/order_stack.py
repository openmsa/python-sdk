"""Module Orderstack."""

import json

from msa_sdk.device import Device


class OrderStack(Device):
    """Class OrderStack."""

    def __init__(self, device_id):
        """Initialize."""
        Device.__init__(self, device_id=device_id)
        self.api_path = '/orderstack'
    

    def add_command_in_stack(self, command: str, params,
                     timeout=300) -> None:
        """

        To push multiple commands in a stack.

        Parameters
        -----------
        command: String
                CRUID method in microservice to add to the stack.

        params: dict
                Parameters in a dict format:

                {
                    "simple_firewall": {
                        "1": {
                                "object_id": "1",
                                "src_ip": "3.4.5.7",
                                "dst_port": "44"
                        },
                        "2": {
                                "object_id": "2",
                                "src_ip": "3.4.5.6",
                                "dst_port": "42"
                        }
                }
                timeout:  int timeout in sec (300 secondes by default)

        Returns
        --------
        None

        """
        self.action = 'Adds a command in the stack'
        self.path = '{}/command/{}/{}'.format(self.api_path,
                                              self.device_id,
                                              command)
        self._call_put(params, timeout)


    def apply_command_stacked(self, timeout=300) -> None:
        """
        Execute all the commands stacked for the device.
        Parameters
        -----------
        device_id: int
                Id of the device.
        timeout: int
                Timeout in seconds (300 seconds by default)
        Returns
        -------
        None
        
        """
        self.action = 'Execute all the commands stacked for the device'
        self.path = '{}/execute/{}'.format(self.api_path, self.device_id)

        self._call_post(timeout=timeout)
