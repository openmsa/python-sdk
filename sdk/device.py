"""Module Device."""
import json

from sdk.msa_api import MSA_API


class DeviceFields(MSA_API):
    """Class Device Fields."""

    def __init__(self, device_id):
        """
        Initialize.

        @param device_id: Device ID
        @type device_id: String

        @return: None
        """
        MSA_API.__init__(self)
        self.api_path = "/deviceFields"
        self.device_id = device_id

    def activate_email_alerting(self):
        """Email alerting."""
        self.path = "{}/{}/emailAlerting".format(self.api_path, self.device_id)

        self.call_put()

    def add_serial_number(self, serial_number):
        """Add Serial Number."""
        self.path = "{}/{}/serialNumber/{}".format(
            self.api_path, self.device_id, serial_number)
        self.call_put()


class Device(MSA_API):  # pylint: disable=too-many-instance-attributes
    """Class Device."""

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, customer_id=None, name=None, manufacturer_id=None,
                 model_id=None, login=None, password=None,
                 password_admin=None, management_address=None,
                 device_external=None, log_enabled=True,
                 log_more_enabled=True, mail_alerting=True,
                 reporting=False, snmp_community="ubiqube", device_id=None):
        """
        Initialize.

        @param customer_id: Customer id
        @param name: Name
        @param manufacturer_id: Manufacture ID
        @param model_id: Model ID
        @param login: Login
        @param password: Password
        @param password_admin: Password Admin
        @param management_address: Management Address
        @param device_external: Device External
        @param log_enabled: Log Enabled
        @param log_more_enabled: More logs
        @param mail_alerting: Mail alerting
        @param reporting: Reporting
        @param snmp_community: SNMP Community
        @param device_id: Device ID

        @return: None
        """
        MSA_API.__init__(self)
        self.customer_id = customer_id
        self.name = name
        self.manufacturer_id = manufacturer_id
        self.model_id = model_id
        self.login = login
        self.password = password
        self.password_admin = password_admin
        self.management_address = management_address
        self.device_external = device_external
        self.log_enabled = log_enabled
        self.log_more_enabled = log_more_enabled
        self.mail_alerting = mail_alerting
        self.reporting = reporting
        self.snmp_community = snmp_community
        self.device_id = device_id
        self.api_path_v1 = "/device/v1"
        self.api_path = "/device"
        self.management_interface = None
        self.use_nat = None
        self.configuration = {}
        self.device_fields = None

    def _format_path_ref_id(self, by_ref, path):
        del_by = "reference" if by_ref else "id"
        self.path = "{}/{}/{}".format(path, del_by, self.device_id)

    def delete(self, by_ref=False):
        """
        Delete device.

        @param by_ref: Path /id/ or /reference/
        @type by_ref: String

        @return: None
        """
        self._format_path_ref_id(by_ref, self.api_path)
        self.call_delete()

    def activate(self):
        """
        Activate device.

        @return: None
        """
        self.path = "{}/activate/{}".format(self.api_path, self.device_id)
        self.call_post()

    def provision(self):
        """
        Provision a device.

        @return: None
        """
        self.path = "{}/provisioning/{}".format(self.api_path, self.device_id)
        self.call_post()

    def provision_status(self):
        """
        Get the provision status.

        @return: Json with provision status
        @rtype: String
        """
        self.path = "{}/provisioning/status/{}".format(
            self.api_path, self.device_id)
        self.call_get()
        return json.dumps(self.response.content)

    def is_device(self):
        """
        Check if is device.

        @return: Json with True or False
        @rtype: String
        """
        self.path = "{}/isDevice/{}".format(self.api_path, self.device_id)
        self.call_get()
        return json.loads(self.response.content)

    def read(self, by_ref=False):
        """
        Read device information.

        @param by_ref: Path /id/ or /reference/
        @type by_ref: String
        @return: None
        """
        self._format_path_ref_id(by_ref, self.api_path)
        self.call_get()
        device_info = json.loads(self.response.content)

        self.name = device_info["name"]
        self.manufacturer_id = device_info["manufacturerId"]
        self.model_id = device_info["modelId"]
        self.management_address = device_info["managementAddress"]
        self.management_interface = device_info["managementInterface"]
        self.login = device_info["login"]
        self.password = device_info["password"]
        self.password_admin = device_info["passwordAdmin"]
        self.log_enabled = device_info["logEnabled"]
        self.mail_alerting = device_info["mailAlerting"]
        self.use_nat = device_info["useNat"]
        self.snmp_community = device_info["snmpCommunity"]
        self.device_fields = DeviceFields(self.device_id)

        return self.response.content

    def status(self):
        """
        Get device status.

        @return: One word string
        @rtype: String
        """
        self.path = "{}/status/{}".format(self.api_path, self.device_id)
        self.call_get()
        return self.response.content

    def get_configuration_status(self):
        """
        Get configuration status and add to device configuration.

        @return: None
        """
        self.path = "{}/configuration/status/id/{}".format(
            self.api_path, self.device_id)
        self.call_get()
        self.configuration = json.loads(self.response.content)

    def update_config(self):
        """
        Update config.

        @return: Config in JSON form
        @rtype: String
        """
        self.path = "{}/configuration/update/{}".format(
            self.api_path, self.device_id)
        self.call_post()
        return json.dumps(self.response.content)

    def ping(self, address):
        """
        Ping address.

        @param address[in] Ip address.
        @return Ping response
        """
        self.path = "{}/ping/{}".format(self.api_path, address)
        self.call_get()

        return self.response.content

    def initial_provisioning(self):
        """
        Initialize provisioning.

        @return: TODO
        """
        self.path = "{}/provisioning/{}".format(self.api_path, self.device_id)
        self.call_post()

    def push_configuration_status(self):
        """
        Push configuration status.

        @return: Json with configuration
        @rtype: String
        """
        self.path = "{}/push_configuration/status/{}".format(
            self.api_path, self.device_id)

        self.call_get()
        return json.dumps(self.response.content)

    def push_configuration(self):
        """
        Push configuration.

        @return: TODO
        """
        self.path = "{}/push_configuration/{}".format(
            self.api_path, self.device_id)

        self.call_put()

    def update_ip_address(self, ip_addr, netmask="255.255.255.255"):
        """
        Update Ip Address.

        @param ip_addr: IP Address format (xxx.xxx.xxx.xxx)
        @type ip_addr: String
        @param netmask: Netmask, default 255.255.255.2555
        @type netmask: String

        @returns: None
        """
        path = "{}/management_ip/update/{}?ip={}&mask={}"
        self.path = path.format(
            self.api_path,
            self.device_id,
            ip_addr,
            netmask)
        self.call_put()

    def profile_switch(self, old_profile, new_profile_ref):
        """
        Profile Switch.

        @param old_profile: Old profile name
        @type old_profile: String
        @param new_profile_ref: New profile name
        @type new_profile_ref: String

        @return: None
        """
        path = ('{}/conf_profile/switch/{}'
                '?old_profile_ref={}&new_profile_ref={}').format(
                    self.api_path,
                    self.device_id,
                    old_profile,
                    new_profile_ref)
        self.path = path
        self.call_put()

    def update_credentials(self, login, password):
        """
        Update Credentials.

        @param login: Credentials Login
        @type login: String
        @param password: Credentials password
        @type password: String
        @return: None
        """
        path = "{}/credentials/update/{}?login={}&password={}"
        self.path = path.format(self.api_path, self.device_id, login, password)
        self.call_put()

    def attach_files(self, uris, position="AUTO"):
        """
        Attach files.

        @param uris:
        @param position:
        @return: None
        """
        self.path = ("{}/attach/{}/files/{}").format(self.api_path,
                                                     self.device_id, position)
        self.call_put(json.dumps(uris))

    def detach_files(self, uris):
        """
        Attach files.

        @param uris:
        @return: None
        """
        self.path = ("{}/detach/{}/files").format(self.api_path,
                                                  self.device_id)
        self.call_put(json.dumps(uris))
