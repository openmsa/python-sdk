"""
Test MSA API
"""

from unittest.mock import MagicMock
from unittest.mock import patch
import json
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


def test_content_no_log():
    """
    Test content with no log
    """

    api = MSA_API()

    response = {
        "wo_status": 'ENDED',
        "wo_comment": 'Task OK',
        "wo_newparams": {"SERVICEINSTANCEID": 1234, "Other": "Value"}
    }

    assert api.content(
        'ENDED', 'Task OK', {
            "SERVICEINSTANCEID": 1234,
            "Other": "Value"}) == json.dumps(response)


def test_content_with_log(tmpdir):
    """
    Test content with no log
    """

    temp_dir = tmpdir.mkdir('test')

    with patch('msa_sdk.msa_api.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = MSA_API()

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params
        }

        assert api.content(
            'ENDED', 'Task OK',
            params,
            True) == json.dumps(response)

        assert json.dumps(params, indent=4) == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()
