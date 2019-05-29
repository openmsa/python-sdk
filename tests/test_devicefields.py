"""
Test Devicefields
"""

from unittest.mock import patch
import pytest

from msa_sdk.device import DeviceFields


@pytest.mark.skip
def test_email_alerting():
    """
    Test Email Alerting
    """

    with patch('requests.put') as mock_call_put:

        device = DeviceFields(device_id='MSADevID')
        device.activate_email_alerting()
        assert device.path == '/deviceFields/{}/emailAlerting'.format(
            device.device_id)
        mock_call_put.assert_called_once()


@pytest.mark.skip
def test_serial_number_put():
    """
    Test serial number
    """

    serial_number = 'SerialNumberabc'

    device = DeviceFields(device_id='MSADevID')
    device.add_serial_number(serial_number)

    assert device.path == ('/DeviceFields/{}/'
                           'serialNumber/{}').format(
                               device.device_id, serial_number)
