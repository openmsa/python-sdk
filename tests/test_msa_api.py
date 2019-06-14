"""
Test MSA API
"""

from unittest.mock import MagicMock
from unittest.mock import patch
import pytest

from msa_sdk.msa_api import MSA_API


def host_port():
    """
    Hostname and port of the API
    """
    return ('api_hostname', '8080')


@pytest.fixture
@patch('requests.post')
@patch('msa_sdk.msa_api.host_port')
def api_fixture(mock_host_port, mock_post):
    """
    API Fixtures
    """
    mock_post.return_value.json.return_value = {'token': '12345qwert'}
    mock_host_port.return_value = host_port()
    api = MSA_API()
    return api


# pylint: disable=redefined-outer-name
def test_hostname_port(api_fixture):
    """
    Test hostname and port
    """
    api = api_fixture

    assert api.url == 'http://api_hostname:8080/ubi-api-rest'


def test_get_token(api_fixture):
    """
    Test Get Token
    """
    api = api_fixture

    assert api.token == '12345qwert'


def test_check_reponse_fail(api_fixture):
    """
    Test response fail
    """
    api = api_fixture
    api.response = MagicMock()
    api.response.ok = False

    with pytest.raises(RuntimeError):
        api.check_response()


def test_check_reponse_ok(api_fixture):
    """
    Test response fail
    """
    api = api_fixture
    api.response = MagicMock()
    api.response.ok = False

    with pytest.raises(RuntimeError):
        api.check_response()
