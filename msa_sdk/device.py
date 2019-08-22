"""Module Device."""
import json

from msa_sdk.msa_api import MSA_API


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

        Parameters
        ----------
        customer_id: String
                Customer id
        name: String
                Name of the device
        manufacturer_id: String
                Manufacture ID
        model_id: String
                Model ID
        login: String
                Login
        password: String
                Password
        password_admin: String
                Password Admin
        management_address: Management Address
        device_external: Device External
        log_enabled: Bool
                Log Enabled
        log_more_enabled: More logs
        mail_alerting: Bool
                Mail alerting
        reporting: Bool
                Reporting
        snmp_community: SNMP Community
        device_id: Device ID

        Returns
        -------
        None

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
        self.api_path_v1 = "/device/v1"
        self.api_path = "/device"
        self.management_interface = None
        self.use_nat = False
        self.configuration = {}
        self.device_id = device_id

        if device_id:
            self.read()

    def _format_path_ref_id(self, by_ref, path):
        del_by = "reference/" + by_ref \
            if by_ref else "id/" + str(self.device_id)
        self.path = "{}/{}".format(path, del_by)

    def create(self):
        """
        Create device.

        Returns
        -------
        None

        """
        self.path = '{}/{}'.format(self.api_path, self.customer_id)

        data = {"manufacturerId": self.manufacturer_id,
                "modelId": self.model_id,
                "managementAddress": self.management_address,
                "reporting": self.reporting,
                "useNat": self.use_nat,
                "logEnabled": self.log_enabled,
                "logMoreEnabled": self.log_more_enabled,
                "managementInterface": self.management_interface,
                "mailAlerting": self.mail_alerting,
                "passwordAdmin": self.password_admin,
                "externalReference": "",
                "login": self.login,
                "name": self.name,
                "password": self.password,
                "id": 0,
                "snmpCommunity": self.snmp_community}

        self.call_post(json.dumps(data))
        self.device_id = json.loads(self.response.content)['entity']['id']
        return json.dumps(data)

    def delete(self, by_ref=False):
        """
        Delete device.

        Parameters
        ----------
        by_ref: String
                Path /id/ or /reference/

        Returns
        -------
        None

        """
        self._format_path_ref_id(by_ref, self.api_path)
        self.call_delete()

    def activate(self):
        """
        Activate device.

        Returns
        --------
        None

        """
        self.path = "{}/activate/{}".format(self.api_path, self.device_id)
        self.call_post()

    def provision(self):
        """
        Provision a device.

        Returns
        --------
        None

        """
        self.path = "{}/provisioning/{}".format(self.api_path, self.device_id)
        self.call_post()

    def provision_status(self):
        """
        Get the provision status.

        Returns
        --------
        Json with provision status

        """
        self.path = "{}/provisioning/status/{}".format(
            self.api_path, self.device_id)
        self.call_get()
        return json.dumps(self.response.content)

    def is_device(self):
        """
        Check if is device.

        Returns
        --------
        Json with True or False

        """
        self.path = "{}/isDevice/{}".format(self.api_path, self.device_id)
        self.call_get()
        return json.loads(self.response.content)

    def read(self, by_ref=False):
        """
        Read device information.

        Parameters
        ----------
        by_ref: String
            Path /id/ or /reference/

        Returns
        --------
        None

        """
        self._format_path_ref_id(by_ref, self.api_path)
        self.call_get()
        device_info = json.loads(self.response.content)

        self.device_id = device_info['id']
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

        return self.response.content

    def status(self):
        """
        Get device status.

        Returns
        --------
        One word string

        """
        self.path = "{}/status/{}".format(self.api_path, self.device_id)
        self.call_get()
        return self.response.content

    def get_configuration_status(self):
        """
        Get configuration status and add to device configuration.

        Returns
        --------
        None

        """
        self.path = "{}/configuration/status/id/{}".format(
            self.api_path, self.device_id)
        self.call_get()
        self.configuration = json.loads(self.response.content)

    def update_config(self):
        """
        Update config.

        Returns
        --------
        Config in JSON form

        """
        self.path = "{}/configuration/update/{}".format(
            self.api_path, self.device_id)
        self.call_post()
        return json.dumps(self.response.content)

    def ping(self, address):
        """
        Ping address.

        Parameters
        ----------
        address: String
                Ip address.

        Returns
        --------
        Ping response

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

        Returns
        --------
        Json with configuration

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

        Parameters
        ----------
        ip_addr: String
                IP Address format (xxx.xxx.xxx.xxx)
        netmask: String
                Netmask, default 255.255.255.2555

        Returns
        --------
        None

        """
        path = "{}/management_ip/update/{}?ip={}&mask={}"
        self.path = path.format(self.api_path, self.device_id, ip_addr,
                                netmask)
        self.call_put()

    def profile_switch(self, old_profile, new_profile_ref):
        """
        Profile Switch.

        Parameters
        ----------
        old_profile: String
                Old profile name
        new_profile_ref: String
            New profile name

        Returns
        --------
        None

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

        Parameters
        ----------
        login: String
                Credentials Login
        password: String
                Credentials password

        Returns
        --------
        None

        """
        path = "{}/credentials/update/{}?login={}&password={}"
        self.path = path.format(self.api_path, self.device_id, login, password)
        self.call_put()

    def attach_files(self, uris, position="AUTO"):
        """
        Attach files.

        Parameters
        ----------
        uris:
        position: String
                default: AUTO

        Returns
        --------
        None

        """
        self.path = ("{}/attach/{}/files/{}").format(self.api_path,
                                                     self.device_id, position)
        self.call_put(json.dumps(uris))

    def detach_files(self, uris):
        """
        Attach files.

        Parameters
        ----------
        uris: String

        Returns
        --------
        None

        """
        self.path = ("{}/detach/{}/files").format(self.api_path,
                                                  self.device_id)
        self.call_put(json.dumps(uris))
