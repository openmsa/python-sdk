"""
Test Device
"""
from unittest.mock import patch
from util import device_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_new_device(device_fixture):
    """
    New device
    """
    device = device_fixture

    assert device.customer_id == 10
    assert device.name == 'MyDevice'
    assert device.manufacturer_id == 11
    assert device.model_id == 13
    assert device.login == 'ncroot'
    assert device.password == 'pswd'
    assert device.password_admin == 'adm_pswd'
    assert device.management_address == 'mng_addres'
    assert device.device_external == 'Dexternal'


def test_delete(device_fixture):
    """
    Test delete
    """
    device = device_fixture
    device.device_id = '1234'
    with patch('requests.delete') as mock_call_delete:

        device.delete()
        assert device.path == '/device/id/{}'.format(device.device_id)
        mock_call_delete.assert_called_once()
