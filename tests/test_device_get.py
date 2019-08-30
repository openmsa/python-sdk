"""
Test Device Get
"""
import json

from unittest.mock import patch
from unittest.mock import MagicMock

from util import _is_valid_json
from util import device_fixture  # pylint: disable=unused-import
from util import device_info
from msa_sdk.device import Device


@patch('requests.post')
def test_read_by_id(mock_post):
    """
    Read Device by id
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = device_info()
        device = Device(device_id=21594)

        assert device.path == '/device/id/21594'
        assert device.device_id == 21594
        assert device.name == "Linux self MSA"
        assert device.manufacturer_id == 14020601
        assert device.model_id == 14020601
        assert device.management_address == '127.0.0.1'
        assert device.management_interface == ''
        assert device.login == 'root'
        assert device.password == '$ubiqube'
        assert device.password_admin == ''
        assert not device.log_enabled
        assert not device.mail_alerting
        assert not device.reporting
        assert device.use_nat
        assert device.snmp_community == ''
        mock_call_get.assert_called_once()


@patch('requests.post')
def test_read_by_reference(mock_post):
    """
    Read Device by reference
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = device_info()
        device = Device()

        assert _is_valid_json(device.read('DEV_REF'))

        assert device.path == '/device/reference/DEV_REF'
        assert device.device_id == 21594
        assert device.name == "Linux self MSA"
        assert device.manufacturer_id == 14020601
        assert device.model_id == 14020601
        assert device.management_address == '127.0.0.1'
        assert device.management_interface == ''
        assert device.login == 'root'
        assert device.password == '$ubiqube'
        assert device.password_admin == ''
        assert not device.log_enabled
        assert not device.mail_alerting
        assert not device.reporting
        assert device.use_nat
        assert device.snmp_community == ''
        mock_call_get.assert_called_once()


def test_status(device_fixture):  # pylint: disable=W0621
    """
    Test Status
    """
    device = device_fixture

    with patch('requests.get') as mock_call_get:

        mock_call_get.return_value.content = 'UNREACHABLE'
        assert device.status() == 'UNREACHABLE'

        assert device.path == '/device/status/{}'.format(device.device_id)
        mock_call_get.assert_called_once()


def test_status_unreachable(device_fixture):  # pylint: disable=W0621
    """
    Test Status UNREACHABLE
    """
    device = device_fixture

    with patch('requests.get') as mock_call_get:

        mock_call_get.return_value.content = 'UNREACHABLE'
        assert device.status() == 'UNREACHABLE'

        assert device.path == '/device/status/{}'.format(device.device_id)


def test_status_fail(device_fixture):  # pylint: disable=W0621
    """
    Test Status fail
    """
    device = device_fixture

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get device status",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')
        device.status()
        assert device.content == json.dumps(fail_response)


def test_provision_status(device_fixture):  # pylint: disable=W0621
    """
    Test provision status
    """

    provision_info = ('{"errorMsg": "", "rawJSONResult": '
                      '"{\"sms_status\": \"OK\",'
                      ' "PROVISIONING_PROCESS\": \"OK\",'
                      ' \"sms_result\": [{\"sms_status\": "OK\",'
                      ' \"sms_stage\": \"Lock Provisioning\",'
                      ' \"sms_message\": \"OK\"}, '
                      '{\"sms_status\": \"OK\", '
                      '\"sms_stage\": \"Initial Connection\", '
                      '"sms_message\": \"OK\"}, {\"sms_status\": \"OK\", '
                      '\"sms_stage\": "Initial Configuration\", '
                      '\"sms_message\": \"OK\"}, {\"sms_status\": "OK\", '
                      '\"sms_stage\": \"DNS Update\", '
                      '\"sms_message\": \"OK\"}, {\"sms_status\": \"OK\", '
                      '\"sms_stage\": \"Unlock Provisioning\",'
                      '\"sms_message\": \"OK\"}, {\"sms_status\": \"OK\", '
                      '\"sms_stage\":\"Save Configuration\",'
                      '\"sms_message\":\"OK\"}]}", "status": "OK"}')

    device = device_fixture
    device.device_id = 1234

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = provision_info

        assert _is_valid_json(device.provision_status())

        mock_call_get.assert_called_once()
        assert device.path == '/device/provisioning/status/1234'


def test_provision_status_fail(device_fixture):  # pylint: disable=W0621
    """
    Test provision status fail
    """

    device = device_fixture

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get provision status",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')
        device.provision_status()
        assert device.content == json.dumps(fail_response)


# pylint: disable=redefined-outer-name
def test_load_configuration(device_fixture):
    """
    Test Load configuration
    """
    device = device_fixture
    device.device_id = 1234

    with patch('requests.get') as mock_call_get:
        r_value = ('{"message":"OK\\r\\n\\r\\n","date":"24-04-2019 '
                   '16:30:05","status":"ENDED"}')
        mock_call_get.return_value.content = r_value
        device.get_configuration_status()

        mock_call_get.assert_called_once()

        assert device.path == '/device/configuration/status/id/1234'
        assert device.configuration['message'] == 'OK\r\n\r\n'
        assert device.configuration['date'] == '24-04-2019 16:30:05'
        assert device.configuration['status'] == 'ENDED'


def test_ping(device_fixture):
    """
    Test ping
    """
    device = device_fixture

    r_value = ('{"message":"--- ::1 ping statistics ---\\n5 packets '
               'transmitted, 5 received, 0% packet loss, '
               'time 3999ms\\nrtt min/avg/max/mdev = 0.014/0.020/0.027/0.007 '
               'ms","rawJSONResult":"{\\"sms_status\\":\\"OK\\",'
               '\\"sms_code\\":\\"\\",\\"sms_message\\":\\"--- ::1 ping '
               'statistics ---\\\\n5 packets transmitted, 5 received, 0% '
               'packet loss, time 3999ms\\\\nrtt min/avg/max/mdev = '
               '0.014/0.020/0.027/0.007 ms\\"}","status":"OK"}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = r_value

        assert _is_valid_json(device.ping('localhost'))

        assert device.path == '/device/ping/localhost'
        mock_call_get.assert_called_once()


def test_push_configuration_status(device_fixture):
    """
    Test push configuration
    """
    device = device_fixture

    r_value = ('{"message":"[root@LINUX-FW ~]# [root@LINUX-FW ~]#\n ",'
               '"date":"27-06-2018 09:15:33","status":"ENDED"}')

    with patch('requests.get') as mock_call_get:

        mock_call_get.return_value.content = r_value
        assert _is_valid_json(device.push_configuration_status())

        assert device.path == '/device/push_configuration/status/{}'.format(
            device.device_id)
        mock_call_get.assert_called_once()


def test_is_device(device_fixture):
    """
    Test is device
    """
    device = device_fixture

    r_value = json.dumps('{"isDevice": true}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = r_value

        assert device.is_device()
        assert device.path == '/device/isDevice/{}'.format(device.device_id)
        mock_call_get.assert_called_once()


def test_is_device_fail(device_fixture):  # pylint: disable=W0621
    """
    Test is device fail
    """

    device = device_fixture

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': 'Is device',
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')
        device.is_device()
        assert device.content == json.dumps(fail_response)
