"""
Test Order Command
"""
import json
from unittest.mock import patch

import pytest
from util import order_fixture  # pylint: disable=unused-import


@patch('msa_sdk.device.Device.read')
def test_command_stack(_, order_fixture):
    """
    Test Command apply command stack
    """

    local_path_command_stack = '/orderstack/command/21594/UPDATE'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        order = order_fixture
        order.command_stack('UPDATE', {"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)

        assert order.path == local_path_command_stack

        print(json.loads(order.content)) 
        mock_call_post.assert_called_with({"1": {"subnet": "mySubnet1"}, "2": {"subnet": "mySubnet2"}}, 50)
        


