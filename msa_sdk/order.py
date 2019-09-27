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