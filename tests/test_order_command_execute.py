"""
Test Order Command
"""
from unittest.mock import patch

import pytest

from util import order_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


@patch('msa_sdk.device.Device.read')
def test_command_execute(_, order_fixture):
    """
    Test Command execute
    """

    local_path = '/ordercommand/execute/21594/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = order_fixture
        order.command_execute('UPDATE', {"subnet": "mySubnet"}, 50)

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"}, 50)


def test_command_execute_fail(order_fixture):
    """
    Test Command execute fail parameters type
    """

    order = order_fixture
    with pytest.raises(TypeError):
        order.command_execute('UPDATE', 123, 50)


@patch('msa_sdk.device.Device.read')
def test_command_generate_configuration(_, order_fixture):
    """
    Test command generate configuration
    """

    local_path = '/ordercommand/get/configuration/21594/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = order_fixture
        order.command_generate_configuration('UPDATE',
                                             {"subnet": "mySubnet"})

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"})


@patch('msa_sdk.device.Device.read')
def test_command_synchronize(_, order_fixture):
    """
    Test command generate configuration
    """

    local_path = '/ordercommand/synchronize/21594'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = order_fixture
        order.command_synchronize(50)

        assert order.path == local_path

        mock_call_post.assert_called_once_with(timeout=50)


@patch('msa_sdk.device.Device.read')
def test_command_call(_, order_fixture):
    """
    Test command call
    """
    local_path = '/ordercommand/call/21594/UPDATE/1'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = order_fixture
        order.command_call('UPDATE', 1,
                           {"subnet": "mySubnet"})

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"})


@patch('msa_sdk.device.Device.read')
def test_command_objects_all(_, order_fixture):
    """
    Get all microservices attached to a device
    """
    local_path = '/ordercommand/objects/21594'
    return_body = [
        'accesslist',
        'addressObject',
        'address_holder'
    ]
    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = return_body
        order = order_fixture
        order.command_objects_all()

        assert order.path == local_path
        assert order.content == return_body


@patch('msa_sdk.device.Device.read')
def test_command_objects_instances(_, order_fixture):
    """
    Get microservices instance by microservice name
    """
    local_path = '/ordercommand/objects/21594/accesslist'
    return_body = [
        '2000 line 1',
        '2000 line 2',
        'FROM-inside line 1'
    ]
    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = return_body
        order = order_fixture
        order.command_objects_instances('accesslist')

        assert order.path == local_path
        assert order.content == return_body


@patch('msa_sdk.device.Device.read')
def test_command_objects_instances_by_id(_, order_fixture):
    """
    Get microservices instance by microservice object ID
    """
    local_path = '/ordercommand/objects/21594/accesslist/2000'
    return_body = {
        "accesslist": {
            "2000": {
                "_order": "1000",
                "destip": "8.8.8.0",
                "destmask": "255.255.255.0",
                "object_id": "2000 line 1",
                "options": "log informational interval 300 ",
                "protocol": "ip",
                "right": "permit",
                "sourceip": "10.101.32.0",
                "sourcemask": "255.255.255.0"
            }
        }
    }
    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = return_body
        order = order_fixture
        order.command_objects_instances_by_id('accesslist', '2000')

        assert order.path == local_path
        assert order.content == return_body
