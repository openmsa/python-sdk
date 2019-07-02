"""Module Order."""

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

        params: dict
              Parameters


        Returns
        -------
        None

        """
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
        self.path = '{}/synchronize/{}'.format(self.api_path,
                                               self.device_id)

        self.call_post(timeout=timeout)
