"""
Test Customer POST
"""
from unittest.mock import patch

from util import customer_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_create_customer_by_prefix(customer_fixture):
    """
    Test create customer by prefix.
    """

    local_path = '/customer/AAAA6?name=name1&reference=reference1'
    params = {}
    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        customer = customer_fixture
        customer.create_customer_by_prefix('AAAA6', "name1", "reference1")

        assert customer.path == local_path
        assert params == {}

        mock_call_post.assert_called_once_with(params)
