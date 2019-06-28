"""
Test Order Command
"""
from unittest.mock import patch
from msa_sdk.order import Order
from util import device_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


@patch('msa_sdk.device.Device.read')
def test_command_execute(_):
    """
    Test Command execute
    """

    local_path = '/ordercommand/execute/1234/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = Order(1234)
        order.command_execute('UPDATE', {"subnet": "mySubnet"}, 50)

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"}, 50)


@patch('msa_sdk.device.Device.read')
def test_command_generate_configuration(_):
    """
    Test command generate configuration
    """

    local_path = '/ordercommand/get/configuration/1234/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = Order(1234)
        order.command_generate_configuration('UPDATE',
                                             {"subnet": "mySubnet"})

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"})


@patch('msa_sdk.device.Device.read')
def test_command_synchronize(_):
    """
    Test command generate configuration
    """

    local_path = '/ordercommand/synchronize/1234'

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        order = Order(1234)
        order.command_synchronize(50)

        assert order.path == local_path

        mock_call_post.assert_called_once_with(timeout=50)
