"""Module Order."""

import json

from msa_sdk.device import Device


class Order(Device):
    """Class Order."""

    def __init__(self, device_id):
        """Initialize."""
        Device.__init__(self, device_id=device_id)
        self.api_path = '/ordercommand'
        self.read()

    def command_execute(self, command, params, timeout=60):
        """

        Command execute.

        Parameteres
        -----------
        command: String
                Order command
                Available values : CREATE, UPDATE, IMPORT, LIST, READ, DELETE

        params: dict
                Parameters in a dict format:
                {"simple_firewall": {
                    "12": {
                            "object_id": "12",
                            "src_ip": "3.4.5.6",
                            "dst_port": "44"
                    }
                }


        Returns
        -------
        None

        """
        self.action = 'Command execute'
        self.path = '{}/execute/{}/{}'.format(self.api_path, self.device_id,
                                              command)

        self.call_post(params, timeout)

    def command_generate_configuration(self, command, params):
        """

        Command generate configuration.

        Parameteres
        -----------
        command: String
                Order command

        params: dict
              Parameters


        Returns
        -------
        None

        """
        self.action = 'Command generate configuration'
        self.path = '{}/get/configuration/{}/{}'.format(self.api_path,
                                                        self.device_id,
                                                        command)

        self.call_post(params)

    def command_synchronize(self, timeout):
        """

        Command synchronize.

        Parameteres
        -----------
        timeout: Integer
              Connection timeout


        Returns
        -------
        None

        """
        self.action = 'Command synchronize'
        self.path = '{}/synchronize/{}'.format(self.api_path,
                                               self.device_id)

        self.call_post(timeout=timeout)

    def command_call(self, command, mode, params):
        """

        Command call.

        Parameters:
        -----------
        command: String
                CRUID method in microservice to call
        mode: Integer
                0 - No application
                1 - Apply to base
                2 - Apply to device
        Returns:
        --------
        None

        """
        self.action = 'Call command'
        self.path = '{}/call/{}/{}/{}'.format(self.api_path,
                                              self.device_id,
                                              command,
                                              mode)
        self.call_post(params)

    def command_objects_all(self):
        """

        Get all microservices attached to a device.

        Parameters:
        -----------
        device_id: Integer
                Device ID of the device
        Returns:
        --------
        List:
                List of names of microservices attached

        """
        self.action = 'Get Microservices'
        self.path = '{}/objects/{}'.format(self.api_path, self.device_id)
        self.call_get()

    def command_objects_instances(self, object_name):
        """

        Get microservices instance by microservice name.

        Parameters:
        -----------
        device_id: Integer
                Device ID of the device
        object_name: String
                Name of microservice
        Returns:
        --------
        List:
                List of object IDs per microservice

        """
        self.action = 'Get Microservice Instances'
        self.path = '{}/objects/{}/{}'.format(self.api_path,
                                              self.device_id,
                                              object_name)
        self.call_get()

        return json.loads(self.content)

    def command_objects_instances_by_id(self, object_name, object_id):
        """

        Get microservices instance by microservice object ID.

        Parameters:
        -----------
        device_id: Integer
                Device ID of the device
        object_name: String
                Name of microservice
        object_id: String
                Object ID of microservice instance
        Returns:
        --------
        List:
                Object of microservice parameters per object ID

        """
        self.action = 'Get Microservice Object Details'
        self.path = '{}/objects/{}/{}/{}'.format(self.api_path,
                                                 self.device_id,
                                                 object_name,
                                                 object_id)
        self.call_get()

        return json.loads(self.content)
