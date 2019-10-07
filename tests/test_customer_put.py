"""
Test Customer PUT
"""
from unittest.mock import patch

from msa_sdk.customer import Customer
from util import customer_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name

def test_update_customer_by_id(customer_fixture):
    """
    Test update customer by ID
    """

    local_path = '/customer/id/6'
    params = {'name':''}
    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        customer = customer_fixture
        customer.update_customer_by_id(6)

        assert customer.path == local_path

        mock_call_put.assert_called_once_with(params)

def test_update_variables_by_reference(customer_fixture):
    """
    Test Update variables by reference.
    """
    local_path = '/customer/reference/AAAA6/variables'
    params = {
        "name": "",
        "value": ""
    }
    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        customer = customer_fixture
        customer.update_variables_by_reference('AAAA6')

        assert customer.path == local_path

        mock_call_put.assert_called_once_with(params)

def test_attach_profile_by_reference(customer_fixture):
    """
    Test attach profile by reference
    """
    local_path = '/customer/AAAA6/attach'
    params = {
        "profile": ""
    }
    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        customer = customer_fixture
        customer.attach_profile_by_reference('AAAA6')

        assert customer.path == local_path

        mock_call_put.assert_called_once_with(params)

def test_detach_profile_by_reference(customer_fixture):
    """
    Test detach profile by reference
    """
    local_path = '/customer/AAAA6/detach'
    params = {
        "profile": ""
    }
    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        customer = customer_fixture
        customer.detach_profile_by_reference('AAAA6')

        assert customer.path == local_path

        mock_call_put.assert_called_once_with(params)
