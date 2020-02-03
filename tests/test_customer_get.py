"""
Test Customer GET
"""
import json
from unittest.mock import patch

from msa_sdk.customer import Customer
from util import customer_fixture  # pylint: disable=unused-import
from util import customer_info

# pylint: disable=redefined-outer-name


@patch('requests.post')
def test_get_customer_by_id(mock_post):
    """
    Get customer info by ID
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = customer_info()
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            customer = Customer()
            customer.get_customer_by_id(6)

        assert customer.path == '/customer/id/6'

        customer_json = json.loads(customer.content)
        assert customer_json['id'] == 6
        assert customer_json['actorId'] == 38
        assert customer_json['name'] == "Electric City 1"

        mock_call_get.assert_called_once()


@patch('requests.post')
def test_get_customer_by_reference(mock_post):
    """
    Get customer info by reference
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = customer_info()
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            customer = Customer()
            customer.get_customer_by_reference('AAAA6')

        assert customer.path == '/customer/reference/AAAA6'

        customer_json = json.loads(customer.content)
        assert customer_json['id'] == 6
        assert customer_json['actorId'] == 38
        assert customer_json['name'] == "Electric City 1"

        mock_call_get.assert_called_once()


@patch('requests.post')
def test_get_variables_by_id(mock_post):
    """
    Get variales by ID
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            customer = Customer()
            customer.get_variables_by_id(6)

        assert customer.path == '/customer/id/6/variables'

        mock_call_get.assert_called_once()


@patch('requests.post')
def test_get_variables_by_name(mock_post):
    """
    Get variales by ID
    """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    with patch('requests.get') as mock_call_get:
        with patch('msa_sdk.msa_api.host_port') as mock_host_port:
            mock_host_port.return_value = ('api_hostname', '8080')
            customer = Customer()
            customer.get_variables_by_name(6, 'variableName')

        assert customer.path == '/customer/id/6/variables/variableName'

        mock_call_get.assert_called_once()
