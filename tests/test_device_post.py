"""
Device for POST
"""

import json

from unittest.mock import patch
from unittest.mock import MagicMock


from util import _is_valid_json
from util import device_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_activate(device_fixture):
    """
    Test activate
    """
    device = device_fixture
    with patch('requests.post') as mock_call_post:
        device.activate()
        assert device.path == '/device/activate/{}'.format(device.device_id)
        mock_call_post.assert_called_once()


def test_provision(device_fixture):
    """
    Test provision
    """
    device = device_fixture
    with patch('requests.post') as mock_call_post:

        device.provision()
        assert device.path == '/device/provisioning/{}'.format(
            device.device_id)
        mock_call_post.assert_called_once()


def test_update_config(device_fixture):
    """
    Test update config
    """
    device = device_fixture

    r_value = ('{"status":"OK","result":"","rawJSONResult":'
               '"{\"sms_status\":\"OK\"}",'
               '"rawSmsResult":null,"ok":true,"code":null,"message":null}')

    with patch('requests.post') as mock_call_post:
        mock_call_post.return_value.content = r_value

        assert _is_valid_json(device.update_config())
        assert device.path == '/device/configuration/update/{}'.format(
            device.device_id)
        mock_call_post.assert_called_once()


def test_do_provisioning(device_fixture):
    """
    Test Do Provisioning
    """
    device = device_fixture

    with patch('requests.post') as mock_call_post:

        device.initial_provisioning()

        assert device.path == '/device/provisioning/{}'.format(
            device.device_id)
        mock_call_post.assert_called_once()


def test_create(device_fixture):
    """
    Test create
    """

    device = device_fixture

    response_content = '{"entity": {"id": 67015, "name": "PyASA27-b"}}'

    with patch('requests.post') as mock_call_post:
        mock_call_post.return_value.content = response_content

        assert _is_valid_json(device.create())
        assert device.path == '/device/{}'.format(device.customer_id)
        assert device.device_id == 67015

        mock_call_post.assert_called_once()


def test_create_fail(device_fixture):
    """
    Test fail create device
    """

    device = device_fixture

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Create device",
        'wo_newparams': "Not found"
    }

    with patch('requests.post') as mock_call_post:
        mock_call_post.return_value = MagicMock(ok=False, reason='Not found')

        assert _is_valid_json(device.create())
        assert device.path == '/device/{}'.format(device.customer_id)
        assert device.content == json.dumps(fail_response)