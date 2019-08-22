"""
Device for PUT
"""
from unittest.mock import patch
from util import _is_valid_json

from util import device_fixture  # pylint: disable=unused-import


# pylint: disable=redefined-outer-name
def test_update_ip_address_no_mask(device_fixture):
    """
    Test Update IP Address no netmask
    """
    device = device_fixture
    ip_addr = '10.10.1.3'

    with patch('requests.put') as mock_call_put:

        device.update_ip_address(ip_addr)
        path = ('/device/management_ip/update/{}?ip={}&mask={}')
        assert device.path == path.format(
            device.device_id, ip_addr, '255.255.255.255')
        mock_call_put.assert_called_once()


def test_update_ip_address_mask(device_fixture):
    """
    Test Update IP Address with netmask
    """
    device = device_fixture
    ip_addr = '10.10.1.3'
    netmask = '255.255.255.254'

    with patch('requests.put') as mock_call_put:

        device.update_ip_address(ip_addr, netmask)
        path = ('/device/management_ip/update/{}?ip={}&mask={}')
        assert device.path == path.format(device.device_id, ip_addr, netmask)
        mock_call_put.assert_called_once()


def test_push_configuration(device_fixture):
    """
    Test push configuration status
    """
    device = device_fixture

    with patch('requests.put') as mock_call_put:

        device.push_configuration()
        path = ('/device/push_configuration/{}')
        assert device.path == path.format(device.device_id)
        mock_call_put.assert_called_once()


def test_configuration_profile_switch(device_fixture):
    """
    Test Configuration profile switch
    """
    device = device_fixture

    with patch('requests.put') as mock_call_put:

        device.profile_switch('oldprof', 'newprof')
        path = ('/device/conf_profile/switch/{}?old_profile_ref={}'
                '&new_profile_ref={}')
        assert device.path == path.format(
            device.device_id, 'oldprof', 'newprof')
        mock_call_put.assert_called_once()


def test_update_credentials(device_fixture):
    """
    Test Update Credentials
    """

    device = device_fixture

    with patch('requests.put') as mock_call_put:

        device.update_credentials('login', 'password')
        path = ('/device/credentials/update/{}?login={}&password={}')
        assert device.path == path.format(
            device.device_id, 'login', 'password')
        mock_call_put.assert_called_once()


def test_attach_files(device_fixture):
    """
    Test Attach Files
    """

    device = device_fixture

    uris = ('[{"uri": "Configuration/ABR/Upload_1",'
            '"uri": "Configuration/ABR/Upload_2"'
            '}]')

    with patch('requests.put') as mock_call_put:
        device.attach_files(uris)
        assert device.path == '/device/attach/{}/files/AUTO'.format(
            device.device_id)
        mock_call_put.assert_called_once()

        device.attach_files(uris, 'ABC')
        assert device.path == '/device/attach/{}/files/ABC'.format(
            device.device_id)


def test_detach_files(device_fixture):
    """
    Test Detach Files
    """

    device = device_fixture

    uris = (
        '[{"uri": "Configuration/ABR/Upload_1",'
        '"uri": "Configuration/ABR/Upload_2"'
        '}]'
    )

    with patch('requests.put') as mock_call_put:
        device.detach_files(uris)
        assert device.path == '/device/detach/{}/files'.format(
            device.device_id)
        mock_call_put.assert_called_once()

