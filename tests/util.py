"""Module test util."""
import json
from unittest.mock import patch

import pytest

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
