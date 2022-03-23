"""
Test Device Get
"""
import json
from unittest.mock import MagicMock
from unittest.mock import patch

from msa_sdk.device import Device
from util import _is_valid_json
from util import device_fixture  # pylint: disable=unused-import
from util import device_info


@patch('requests.post')
def test_read_by_id(mock_post):
    """
    Read Device by id
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info()
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            device = Device(device_id=21594)

        assert device.path == '/device/v2/21594'
        assert device.device_id == 21594
        assert device.name == "Linux self MSA"
        assert device.manufacturer_id == 14020601
        assert device.model_id == 14020601
        assert device.management_address == '127.0.0.1'
        assert device.management_port == '22'
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
def test_read_by_invalid_id(mock_post):
    """
    Read Device by id
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_return = {
        "errorCode": 500,
        "message": "Not found"
    }

    return_message = {"wo_status": "FAIL", "wo_comment": "Read device",
                      "wo_newparams": "Not found"}
    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False)
        mock_call_get.return_value.json.return_value = fail_return
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            device = Device(device_id=21594)
        mock_call_get.assert_called_once()
        assert device.content == json.dumps(return_message)


@patch('requests.post')
def test_read_by_reference(mock_post):
    """
    Read Device by reference
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info()
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            device = Device()

        assert _is_valid_json(device.read('DEV_REF'))

        assert device.path == '/device/reference/DEV_REF'
        assert device.device_id == 21594
        assert device.name == "Linux self MSA"
        assert device.manufacturer_id == 14020601
        assert device.model_id == 14020601
        assert device.management_address == '127.0.0.1'
        assert device.management_port == '22'
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
        mock_call_get.return_value.text = 'UNREACHABLE'
        assert device.status() == 'UNREACHABLE'

        assert device.path == '/device/status/{}'.format(device.device_id)
        mock_call_get.assert_called_once()


def test_status_unreachable(device_fixture):  # pylint: disable=W0621
    """
    Test Status UNREACHABLE
    """
    device = device_fixture

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = 'UNREACHABLE'
        assert device.status() == 'UNREACHABLE'

        assert device.path == '/device/status/{}'.format(device.device_id)


def test_status_fail(device_fixture):  # pylint: disable=W0621
    """
    Test Status fail
    """
    device = device_fixture

    fail_return = {
        "errorCode": 500,
        "message": "Not found"
    }

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get device status",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False)
        mock_call_get.return_value.json.return_value = fail_return
        device.status()
        assert device.content == json.dumps(fail_response)


def test_provision_status(device_fixture):  # pylint: disable=W0621
    """
    Test provision status
    """

    provision_info = ('{"errorMsg": "", "rawJSONResult": '
                      '{\"sms_status\": \"OK\",'
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
                      '\"sms_message\":\"OK\"}]}, "status": "OK"}')

    device = device_fixture
    device.device_id = 1234

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = provision_info

        assert _is_valid_json(json.dumps(device.provision_status()))

        mock_call_get.assert_called_once()
        assert device.path == '/device/provisioning/status/1234'


def test_provision_status_fail(device_fixture):  # pylint: disable=W0621
    """
    Test provision status fail
    """

    device = device_fixture

    fail_return = {
        "errorCode": 500,
        "message": "Not found"
    }

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get provision status",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')
        mock_call_get.return_value.json.return_value = fail_return
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
        mock_call_get.return_value.text = r_value
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
        mock_call_get.return_value.text = r_value

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
        mock_call_get.return_value.text = r_value
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
        mock_call_get.return_value.text = r_value

        assert device.is_device()
        assert device.path == '/device/isDevice/{}'.format(device.device_id)
        mock_call_get.assert_called_once()


def test_is_device_fail(device_fixture):  # pylint: disable=W0621
    """
    Test is device fail
    """

    device = device_fixture

    fail_return = {
        "errorCode": 500,
        "message": "Not found"
    }

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': 'Is device',
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')
        mock_call_get.return_value.json.return_value = fail_return
        device.is_device()
        assert device.content == json.dumps(fail_response)


def test_get_configuration_variable(device_fixture):
    """
    Test if configuration variable got successfully
    """

    device = device_fixture

    test_requested_var = 'HTTP_HEADER'
    test_response = json.dumps({
        'name': 'HTTP_HEADER',
        'value': 'Content-Type: application/json',
        'comment': ''
    })
    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = test_response
        assert device.get_configuration_variable(
            test_requested_var)['name'] == test_requested_var


def test_execute_command_on_device(device_fixture):
    """
    Test execute_command_on_device on virtual device
    """

    device    = device_fixture
    device_id = 133
    device.device_id = device_id
    response_content = '{"device_id": 133}'
    #    "response": "{'status': 'OK', 'result': 'show version\\nCisco I...V#', 'rawJSONResult': '{\"sms_status\":\"OK\",\"sms_result\":\"show version\\\\nCisco IOS XE So...', 'rawSmsResult': 'show ...', 'code': 'OK', 'ok': True, 'message': 'Successfully processed'}"


    command = 'show user'

    with patch('requests.get') as mock_call_post:
      mock_call_post.return_value.text = response_content
      assert _is_valid_json(json.dumps(device.execute_command_on_device(command)))
      path = ('/device/v1/command/execute/{}')
      assert path.format(device_id) in device.path 
      assert device.device_id == device_id
      assert not device.fail

      mock_call_post.assert_called_once()
      
      
def test_get_all_configuration_variables(device_fixture):  # pylint: disable=W0621
    """
    Test get_all_configuration_variables
    """
    device = device_fixture

    r_value = json.dumps('{"get_all_configuration_variables": true}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = r_value
        
        assert device.get_all_configuration_variables()
        assert device.path == '/variables/{}'.format(device.device_id)
        mock_call_get.assert_called_once()


def test_get_all_manufacturers(device_fixture):
    """
    Test get_all_manufacturers
    """
    device = device_fixture

    r_value = json.dumps('{"get_all_manufacturers": true}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = r_value
        
        assert device.get_all_manufacturers()
        assert device.path == '/device/v1/manufacturers'
        mock_call_get.assert_called_once()


def test_get_customer_id(device_fixture):
    """
    Test get_customer_id
    """
    device = device_fixture

    r_value = json.dumps('{"get_customer_id": true}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = r_value
        
        assert device.get_customer_id()
        assert device.path == '/device/v1/customer/{}'.format(device.device_id)
        mock_call_get.assert_called_once()

 
      