"""Module test util."""
import json
from unittest.mock import patch

import pytest

from msa_sdk.customer import Customer
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
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
        '"modelId":14020601,"managementAddress":"127.0.0.1",'
        '"managementInterface":"","login":"root",'
        '"password":"$ubiqube","passwordAdmin":"","logEnabled":false,'
        '"logMoreEnabled":false,"mailAlerting":false,"reporting":false,'
        '"useNat":true,"snmpCommunity":""}')

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
          '"comment": "string","modelId": 0,"vendorId": 0}'
    )

@pytest.fixture
def device_fixture():
    """Device fixture."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}

        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            device = Device(10, "MyDevice", 11, 13, "ncroot", "pswd",
                            "adm_pswd", "mng_addres", "Dexternal")
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
            mock_call_get.return_value.content = device_info()

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
