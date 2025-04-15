"""Module test util."""
import json
from unittest.mock import patch

import pytest

from msa_sdk.admin import Admin
from msa_sdk.conf_backup import ConfBackup
from msa_sdk.conf_profile import ConfProfile
from msa_sdk.customer import Customer
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.profile import Profile
from msa_sdk.repository import Repository


def _is_valid_json(msg_json):
    try:
        json.loads(msg_json)
    except ValueError:
        return False
    return True


def device_info():
    """

    Devive information.

    Returns
    -------
    String: a mock device

    """
    return (
        '{"id": 21594, "name": "Linux self MSA",'
        '"externalReference":"MSA21594","manufacturerId":14020601,'
        '"modelId":14020601,"managementAddress":"127.0.0.1","managementPort":"22",'
        '"managementInterface":"","login":"root",'
        '"password":"$ubiqube","passwordAdmin":"","logEnabled":false,'
        '"logMoreEnabled":false,"mailAlerting":false,"reporting":false,'
        '"useNat":true,"snmpCommunity":"","hostname":"test"}')


def device_list():
    """

    Retrieve device list of particular customer.

    Returns
    -------
    String: list of mocked device ids

    """
    return (
        '[{"prefix":"FST","id":130,"name":"BNG-1","sdType":{"id":0,"isObsolete":false,'
        '"useWizard":true,"key":"SdType_1_113","manId":1,"manufacturer":"Cisco","model":"IOS",'
        '"modId":113,"supportedProfiles":"NULL,DES,3DES","type":0,"familyId":0,"proxy":false,'
        '"managed":true,"hasBeenDeleted":false,"utm":false,"reportMail":false,"reportFirewall":false,'
        '"stringyfiedIdent":"CiscoIOS","typeHS":"H","name":"CiscoIOS"},"alertMail":true,"silver":false,'
        '"gold":false,"report":false,"tamper":false,"ha":false,"dmz":false,"modelFromAsset":"CiscoIOSv",'
        '"managed":true,"confProfile":false,"planningProfile":false,"externalReference":"FST130",'
        '"groupId":0,"groupName":"","maintenanceMode":false,"modId":113,"manId":1,"customerId":6,'
        '"monitorPflId":[],"haPeerId":null,"visibleName":"BNG-1-FST130","ubiId":"FST130",'
        '"deviceId":{"id":130,"prefix":"FST","ubiId":"FST130","name":"BNG-1","externalReference":"FST130",'
        '"operatorId":0,"displayName":"BNG-1-FST130","displayNameForJsps":"BNG-1-FST130","type":"","hostname":null},'
        '"idAsLong":130,"pingStatus":"OK"},{"prefix":"FST","id":127,"name":"M2K-1","sdType":{"id":0,"isObsolete":false,'
        '"useWizard":true,"key":"SdType_1_113","manId":1,"manufacturer":"Cisco","model":"IOS","modId":113,'
        '"supportedProfiles":"NULL,DES,3DES","type":0,"familyId":0,"proxy":false,"managed":true,"hasBeenDeleted":false,'
        '"utm":false,"reportMail":false,"reportFirewall":false,"stringyfiedIdent":"CiscoIOS","typeHS":"H",'
        '"name":"CiscoIOS"},"alertMail":true,"silver":false,"gold":false,"report":false,"tamper":false,"ha":false,'
        '"dmz":false,"modelFromAsset":"CiscoIOSv","managed":true,"confProfile":false,"planningProfile":false,'
        '"externalReference":"FST127","groupId":0,"groupName":"","maintenanceMode":false,"modId":113,"manId":1,'
        '"customerId":6,"monitorPflId":[],"haPeerId":null,"visibleName":"M2K-1-FST127","ubiId":"FST127",'
        '"deviceId":{"id":127,"prefix":"FST","ubiId":"FST127","name":"M2K-1","externalReference":"FST127","operatorId":0,'
        '"displayName":"M2K-1-FST127","displayNameForJsps":"M2K-1-FST127","type":"","hostname":null},"idAsLong":127,'
        '"pingStatus":"OK"},{"prefix":"FST","id":125,"name":"M2K-2","sdType":{"id":0,"isObsolete":false,"useWizard":true,'
        '"key":"SdType_1_113","manId":1,"manufacturer":"Cisco","model":"IOS","modId":113,"supportedProfiles":"NULL,DES,3DES",'
        '"type":0,"familyId":0,"proxy":false,"managed":true,"hasBeenDeleted":false,"utm":false,"reportMail":false,'
        '"reportFirewall":false,"stringyfiedIdent":"CiscoIOS","typeHS":"H","name":"CiscoIOS"},"alertMail":false,"silver":false,'
        '"gold":false,"report":false,"tamper":false,"ha":false,"dmz":false,"modelFromAsset":"CiscoIOSv","managed":true,'
        '"confProfile":false,"planningProfile":false,"externalReference":"FST125","groupId":0,"groupName":"",'
        '"maintenanceMode":false,"modId":113,"manId":1,"customerId":6,"monitorPflId":[],"haPeerId":null,'
        '"visibleName":"M2K-2-FST125","ubiId":"FST125","deviceId":{"id":125,"prefix":"FST","ubiId":"FST125",'
        '"name":"M2K-2","externalReference":"FST125","operatorId":0,"displayName":"M2K-2-FST125",'
        '"displayNameForJsps":"M2K-2-FST125","type":"","hostname":null},"idAsLong":125,"pingStatus":"OK"}]')


def customer_info():
    """

    Retrieve Customer information.

    Returns
    -------
    String: a mock device

    """
    return (
        '{"id":6,"actorId":38,"name":"Electric City 1",'
        '"address":{"streetName1":"","streetName2":"","streetName3":"",'
        '"city":"","zipCode":"","country":"","fax":"","email":"prnkikiki@ubiqube.com",'
        '"phone":""},"baseRole":{"id":5,"name":"Abonne"},'
        '"civility":null,"company":false,'
        '"contact":[{"id":84,"name":"","firstName":"","address":'
        '{"streetName1":"Electronic city","streetName2":"phase1","streetName3":"",'
        '"city":"","zipCode":"","country":"","fax":"","email":"prnkikiki@ubiqube.com",'
        '"phone":""}}],"externalReference":"PRNA6","firstname":"",'
        '"login":"PRNCustme6","pwd":"","operatorPrefix":"PRN"}')


def microservice_info():
    """

    Retrieve Microservice information.

    Returns
    -------
    String: a mock microservice

    """
    return (
        '{"information": {"displayName": "string","icon": "string","description": "string",'
        '"category": "string","displayField": "string","order": 0,"visibility": "5"},'
        '"variables": {"variable": [{"defaultValue": "string","displayName": "string",'
        '"name": "string","startIncrement": 0,"type": "string","value": [{}]}],"frozen": 0'
        '},"example": {"content": "string"},"command": [{"name": "string","operation": "string",'
        '"parser": {"section": [{"regexp": "string"}],"lines": {"line": [{"array": {'
        '"name": "string","regexp": "string","mregexp": "string"}}],"ignoreRegexp": {'
        '"regexp": "string"}}},"postTemplate": "string"}],"metaInformationList": [{'
        '"type": "FOLDER","uri": "string","file": true,"name": "string","displayName": "string",'
        '"repositoryName": "string","parentURI": "string","fileType": "text","tag": "string",'
        '"comment": "string","modelId": 0,"vendorId": 0}')


def conf_profile_info():
    """

    Retrieve Configuration Profile information.

    Returns
    -------
    String: a mock configuration profile

    """
    return (
        '{"id":148,"name":"Test Linux","comment":"This is Comment","externalReference":"htoPR148",'
        '"vendor":{"name":"Linux","id":14020601},"model":{"name":"Generic","id":14020601},'
        '"attachedManagedEntities":[202],"microserviceUris":{'
        '"CommandDefinition/LINUX/SYSTEM/user.xml":{"name":"user","groups":[""]}},'
        '"templateUris":[],"dateCreated":"2021-03-15 07:59:04.600040",'
        '"lastUpdate":"2021-03-15 07:59:04.977353","operatorId":3,"customerIds":[9]}')


@pytest.fixture
def device_fixture():
    """Device fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            device = Device(
                10,
                "MyDevice",
                11,
                13,
                "ncroot",
                "pswd",
                "adm_pswd",
                "mng_addres",
                "Dexternal",
                management_port="22")
        device.log_response = False
    return device


@pytest.fixture
def repository_fixture():
    """Repository fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            repos = Repository()
    return repos


@pytest.fixture
def admin_fixture():
    """Admin fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            repos = Admin()
    return repos


@pytest.fixture
def orchestration_fixture():
    """Orchestration fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            orch = Orchestration('MSAA19224')
    return orch


@pytest.fixture
def order_fixture():
    """Order fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('requests.get') as mock_call_get:
            mock_call_get.return_value.text = device_info()

            with patch('msa_sdk.msa_api.host_port') as mock_host_port:
                mock_host_port.return_value = ('api_hostname', '8080')
                order = Order(1234)
    return order


@pytest.fixture
def customer_fixture():
    """Create Customer fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            cust = Customer()
    return cust


@pytest.fixture
def conf_profile_fixture():
    """Confprofile fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('requests.get') as mock_call_get:
            mock_call_get.return_value.text = conf_profile_info()

            with patch('msa_sdk.msa_api.host_port') as mock_host_port:
                mock_host_port.return_value = ('api_hostname', '8080')
                conf_profile = ConfProfile(100)
    return conf_profile

@pytest.fixture
def profile_fixture():
    """Profile fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            profile = Profile()
    return profile


@pytest.fixture
def conf_backup_fixture():
    """Confbackup fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            conf_backup = ConfBackup()
    return conf_backup
