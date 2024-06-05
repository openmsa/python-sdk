"""
Test Customer Delete
"""
from unittest.mock import patch


from msa_sdk.customer import Customer

from msa_sdk.customer import Customer


def test_delete_customer_by_id(customer_fixture):
    """
    Test delete customer by ID
    """

    customer = customer_fixture
    local_path = '/customer/id/6'
    with patch('requests.delete') as mock_call_delete:
        customer.delete_customer_by_id(6)
        assert customer.path == local_path
        mock_call_delete.assert_called_once()


def test_delete_customer_by_reference(customer_fixture):
    """
    Test delete customer by reference
    """

    customer = customer_fixture
    local_path = '/customer/reference/AAAA6'
    with patch('requests.delete') as mock_call_delete:
        customer.delete_customer_by_reference('AAAA6')
        assert customer.path == local_path
        mock_call_delete.assert_called_once()


def test_delete_variable_by_name(customer_fixture):
    """
    Test delete variable by name
    """

    customer = customer_fixture
    local_path = '/customer/id/6/variables/variableName'
    with patch('requests.delete') as mock_call_delete:
        customer.delete_variable_by_name(6, 'variableName')
        assert customer.path == local_path
        mock_call_delete.assert_called_once()
