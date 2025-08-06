"""
Test Order Stack
"""
import json
from unittest.mock import patch

import pytest
from util import orderstack_fixture  # pylint: disable=unused-import


@patch('msa_sdk.device.Device.read')
def test_add_command_in_stack(_, orderstack_fixture):
    """
    Test Add command in the stack
    """

    local_path_command_stack = '/orderstack/command/21594/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        orderstack = orderstack_fixture
        orderstack.add_command_in_stack('UPDATE', {"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)

        assert orderstack.path == local_path_command_stack

        mock_call_put.assert_called_once_with({"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)
        

@patch('msa_sdk.device.Device.read')
def test_apply_command_stacked(_, orderstack_fixture):
    """
    Test Apply command in the stack
    """

    local_path_apply = '/orderstack/execute/21594'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orderstack = orderstack_fixture
        orderstack.apply_command_stacked(timeout=50)

        assert orderstack.path == local_path_apply

        mock_call_post.assert_called_once_with(timeout=50)
