"""Module Order."""

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

        To queue multiple commands in a stack.

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


    def apply_commands_stacked(self, command: str, params: dict, timeout=300) -> None:
        """
        Apply all commands stack of a device.
        Parameters
        -----------
        command: String
                Apply command
                Available values : CREATE, UPDATE, IMPORT, LIST, READ, DELETE
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
        -------
        None
        """
        self.action = 'Execute all the commands stacked'
        self.path = '{}/command/{}/{}'.format(self.api_path, self.device_id,
                                              command)

        self._call_post(params, timeout)


