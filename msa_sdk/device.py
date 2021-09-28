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
                 reporting=False, snmp_community="ubiqube",
                 device_id=None, management_port=None):
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
        management_port: Management Port
        fail: Bool
              Fail creating the device


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
        self.management_port = management_port
        self.fail = None

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
        Dict() with created device capabilities

        """
        self.action = 'Create device'
        self.path = '{}/v2/{}'.format(self.api_path, self.customer_id)

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
                "externalReference": self.device_external,
                "login": self.login,
                "name": self.name,
                "password": self.password,
                "id": 0,
                "snmpCommunity": self.snmp_community}
        if self.management_port:
            data["managementPort"] = self.management_port

        self._call_post(data)
        self.fail = not self.response.ok
        if self.response.ok:
            self.device_id = json.loads(self.content)['id']

        return json.loads(self.content)

    def update(self, field: str, value: str) -> dict:
        """
        Update device.

        field: String
               Modifyed device field
        value: String
               Modified field's value (str)


        Returns
        -------
        Updated device capabilities: Dict()

        """
        self.action = 'Update device'

        data = {"id": self.device_id,
                "name": self.name,
                "manufacturerId": self.manufacturer_id,
                "modelId": self.model_id,
                "managementAddress": self.management_address,
                "managementInterface": self.management_interface,
                "managementPort": self.management_port,
                "login": self.login,
                "password": self.password,
                "password_admin": self.password_admin,
                "log_enable": self.log_enabled,
                "mailAlerting": self.mail_alerting,
                "useNat": self.use_nat,
                "snmpCommunity": self.snmp_community
                }
        self.path = '{}/v2/{}'.format(self.api_path, self.device_id)

        data[field] = value

        self._call_put(json.dumps(data))

        return json.loads(self.content)

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
        self.action = 'Delete device'
        self._format_path_ref_id(by_ref, self.api_path)
        self._call_delete()

    def activate(self):
        """
        Activate device.

        Returns
        --------
        None

        """
        self.path = "{}/activate/{}".format(self.api_path, self.device_id)
        self._call_post()

    def provision(self):
        """
        Provision a device.

        Returns
        --------
        None

        """
        self.action = 'Post Provisioning'
        self.path = "{}/provisioning/{}".format(self.api_path, self.device_id)
        self._call_post()

    def provision_status(self):
        """
        Get the provision status.

        Returns
        --------
        Dict() with provision status

        """
        self.action = 'Get provision status'
        self.path = "{}/provisioning/status/{}".format(
            self.api_path, self.device_id)
        self._call_get()

        return json.loads(self.content)

    def is_device(self):
        """
        Check if is device.

        Returns
        --------
        Dict() with True or False

        """
        self.action = 'Is device'
        self.path = "{}/isDevice/{}".format(self.api_path, self.device_id)
        self._call_get()
        return json.loads(self.content)

    def read(self, by_ref=False):
        """
        Read device information.

        Parameters
        ----------
        by_ref: String
            Path /id/ or /reference/

        Returns
        --------
        Json formated string

        """
        self.action = 'Read device'

        if by_ref:
            self.path = "{}/{}".format(self.api_path,
                                       "reference/{}".format(by_ref))
        else:
            self.path = '{}/v2/{}'.format(self.api_path, self.device_id)

        self._call_get()
        if not self.response.ok:
            return False

        device_info = json.loads(self.content)

        self.device_id = device_info['id']
        self.name = device_info["name"]
        self.manufacturer_id = device_info["manufacturerId"]
        self.model_id = device_info["modelId"]
        self.management_address = device_info["managementAddress"]
        self.management_interface = device_info["managementInterface"]
        self.management_port = device_info["managementPort"]
        self.login = device_info["login"]
        self.password = device_info["password"]
        self.password_admin = device_info["passwordAdmin"]
        self.log_enabled = device_info["logEnabled"]
        self.mail_alerting = device_info["mailAlerting"]
        self.use_nat = device_info["useNat"]
        self.snmp_community = device_info["snmpCommunity"]

        return self.content

    def status(self):
        """
        Get device status.

        Returns
        --------
        One word string

        """
        self.action = "Get device status"
        self.path = "{}/status/{}".format(self.api_path, self.device_id)

        self._call_get()
        return self.content

    def get_configuration_status(self):
        """
        Get configuration status and add to device configuration.

        Returns
        --------
        None

        """
        self.action = 'Get configuration status'
        self.path = "{}/configuration/status/id/{}".format(
            self.api_path, self.device_id)
        self._call_get()
        self.configuration = json.loads(self.content)

    def update_config(self):
        """
        Update config.

        Returns
        --------
        Config in JSON form

        """
        self.action = 'Update config'
        self.path = "{}/configuration/update/{}".format(
            self.api_path, self.device_id)
        self._call_post()
        return json.dumps(self.content)

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
        self.action = 'Get ping'
        self.path = "{}/ping/{}".format(self.api_path, address)
        self._call_get()

        return self.content

    def initial_provisioning(self):
        """
        Initialize provisioning.

        Returns
        --------
        None

        """
        self.action = 'Intial provisioning'
        self.path = "{}/provisioning/{}".format(self.api_path, self.device_id)
        self._call_post()

    def push_configuration_status(self):
        """
        Push configuration status.

        Returns
        --------
        Json with configuration

        """
        self.action = 'Push configuration status'
        self.path = "{}/push_configuration/status/{}".format(
            self.api_path, self.device_id)

        self._call_get()
        return json.dumps(self.content)

    def push_configuration(self, configuration=None):
        """
        Push configuration.

        Parameters
        ----------
        configuration: String
                Configuration parameters for the device

        Returns
        --------
        None

        """
        self.action = 'Push configuration'
        self.path = "{}/push_configuration/{}".format(
            self.api_path, self.device_id)

        self._call_put(configuration)

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
        self.action = 'Update ip address'
        path = "{}/management_ip/update/{}?ip={}&mask={}"
        self.path = path.format(self.api_path, self.device_id, ip_addr,
                                netmask)
        self._call_put()

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
        self.action = 'Profile switch'
        path = ('{}/conf_profile/switch/{}'
                '?old_profile_ref={}&new_profile_ref={}').format(
                    self.api_path,
                    self.device_id,
                    old_profile,
                    new_profile_ref)
        self.path = path
        self._call_put()

    def profile_attach(self, profile_reference: str) -> None:
        """
        Attach new profile to device.

        Parameters
        ----------
        profile_reference:  String
                            Profile external reference

        Returns
        --------
        None

        """
        self.path = ('/profile/{profile_reference}/attach'
                     '?device={device_reference}').format(
                         profile_reference=profile_reference,
                         device_reference=self.device_external)
        self._call_put()

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
        self.action = 'Update credentials'
        path = "{}/credentials/update/{}?login={}&password={}"
        self.path = path.format(self.api_path, self.device_id, login, password)
        self._call_put()

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
        self.action = 'Attach files'
        self.path = ("{}/attach/{}/files/{}").format(self.api_path,
                                                     self.device_id, position)
        self._call_put(json.dumps(uris))

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
        self.action = 'Detach files'
        self.path = ("{}/detach/{}/files").format(self.api_path,
                                                  self.device_id)
        self._call_put(json.dumps(uris))

    def get_configuration_variable(self, name: str) -> dict:
        """
        Get configuration variable value.

        Parameters
        ----------
        name:    String
                 Variable name

        Returns
        -------
        String:  Dict() like {'name': str(), 'value': str(), 'comment': str()}

        """
        self.path = '/variables/{device_id}/{name}'.format(
            device_id=self.device_id, name=name)
        self._call_get()

        return json.loads(self.content)

    def create_configuration_variable(
            self,
            name: str,
            value: str,
            conf_type: str = 'String',
            comment: str = '') -> bool:
        """
        Create configuration variable.

        Parameters
        ----------
        name:    String
                 Variable name
        value:   String
                 Vriable Value
        conf_type:    String
                      Variable type
                      Default: String
        comment: String
                 Comment
                 Default: empty stirng

        Returns
        -------
        True:  Variable has been created successdully
        False: Variable has not been created successfully

        """
        self.path = '/variables/{device_id}/{name}'\
                    '?value={value}'\
                    '&type={type}'\
                    '&comment={comment}'.format(device_id=self.device_id,
                                                name=name,
                                                value=value,
                                                type=conf_type,
                                                comment=comment)

        self._call_put()

        if self.get_configuration_variable(name)['value'] == value:
            return True
        else:
            return False

    def run_jsa_command_device(
            self,
            command: str ) -> bool:
        """
        MSA SDK method to 'Sends jsa command to a device' (POST /sms/cmd/{command}/{id}).

        Parameters
        ----------
        command: String
                  the Jsa command
        device_id: String
                   device_id

        Returns
        -------
        the result
        
        """
        self.action = 'Sends jsa command to a device'
        self.path = '/sms/cmd/{command}/{device_id}/'.format(self.api_path, command=command, device_id=self.device_id )

        self._call_post()
        return json.dumps(self.content)


