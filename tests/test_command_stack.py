"""
Test Order Command Stack
"""
import json
from unittest.mock import patch

import pytest
from util import order_fixture  # pylint: disable=unused-import


@patch('msa_sdk.device.Device.read')
def test_command_execute(_, order_fixture):
    """
    Test Command execute
    """

    local_path = '/ordercommand/execute/21594/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        order = order_fixture
        order.command_execute('UPDATE', {"subnet": "mySubnet"}, 50)

        assert order.path == local_path

        mock_call_post.assert_called_once_with({"subnet": "mySubnet"}, 50)


@patch('msa_sdk.device.Device.read')
def test_apply_command_stack(_, order_fixture):
    """
    Test Command apply command stack
    """

    local_path_command_stack = '/orderstack/command/21594/UPDATE'
    local_path_apply = '/orderstack/execute/21594'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        order = order_fixture
        order.command_stack('UPDATE', {"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)
        assert order.path == local_path_command_stack
        mock_call_post.assert_called_with({"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)
        order.apply_command_stack()
        assert order.path == local_path_apply

        


