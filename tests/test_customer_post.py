"""
Test Customer POST
"""
from unittest.mock import patch

from msa_sdk.customer import Customer
from util import customer_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name

def test_create_customer_by_prefix(customer_fixture):
    """
    Test create customer by prefix.
    """

    local_path = '/customer/AAAA6'
    params = {'name':'', 'reference':''}
    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        customer = customer_fixture
        customer.create_customer_by_prefix('AAAA6')

        assert customer.path == local_path

        mock_call_post.assert_called_once_with(params)
