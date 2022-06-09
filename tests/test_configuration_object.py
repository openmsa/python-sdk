"""
Test Repository
"""
from unittest.mock import patch

from msa_sdk.configuration_object import ConfigurationObject


def test_delete_device():
    """
    Test Delete device
    """

    with patch('msa_sdk.msa_api.MSA_API._call_delete') as mock_call_delete:
        conf_object = ConfigurationObject()

        conf_object.delete(200)

        assert conf_object.path == "/configuration-objects/200"
        mock_call_delete.assert_called_once_with()


def test_delete_device_object():
    """
    Tetst Delete Device Object
    """

    with patch('msa_sdk.msa_api.MSA_API._call_delete') as mock_call_delete:
        conf_object = ConfigurationObject()

        conf_object.delete(200, 'ObjectName')

        assert conf_object.path == "/configuration-objects/200/ObjectName"
        mock_call_delete.assert_called_once_with()
