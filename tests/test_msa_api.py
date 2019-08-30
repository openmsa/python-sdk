"""
Test MSA API
"""

from unittest.mock import patch
import json
import datetime
import pytest

from msa_sdk.msa_api import MSA_API
from util import host_port


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


def test_content_no_log(api_fixture):
    """
    Test content with no log
    """

    api = api_fixture

    response = {
        "wo_status": 'ENDED',
        "wo_comment": 'Task OK',
        "wo_newparams": {"SERVICEINSTANCEID": "1234", "Other": "Value"}
    }

    assert api.show_content(
        'ENDED', 'Task OK', {
            "SERVICEINSTANCEID": "1234",
            "Other": "Value"}) == json.dumps(response)


def test_content_with_log(api_fixture, tmpdir):
    """
    Test content with log
    """

    temp_dir = tmpdir.mkdir('test')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params
        }

        assert api.show_content('ENDED', 'Task OK', params,
                                True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg = '\n=== {} ===\n{}'.format(log_time, json.dumps(params,
                                                                 indent=4))

        assert log_msg == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()


def test_content_with_log_more_lines(api_fixture, tmpdir):
    """
    Test content with log with more lines
    """

    temp_dir = tmpdir.mkdir('test')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params1 = {"SERVICEINSTANCEID": 1234, "Other": "Value1"}
        params2 = {"SERVICEINSTANCEID": 1234, "Other": "Value2"}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params1
        }

        assert api.show_content('ENDED', 'Task OK', params1,
                                True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg_1 = '\n=== {} ===\n{}'.format(log_time, json.dumps(params1,
                                                                   indent=4))

        assert log_msg_1 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()

        api.show_content('ENDED', 'Task OK', params2, True)

        log_msg_2 = '{}\n=== {} ===\n{}'.format(
            log_msg_1, log_time, json.dumps(params2, indent=4))

        assert log_msg_2 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()


def test_constants(api_fixture):
    """
    Test Constants
    """
    msa = api_fixture

    assert msa.ENDED == 'ENDED'
    assert msa.FAILED == 'FAIL'
    assert msa.RUNNING == 'RUNNING'
    assert msa.WARNING == 'WARNING'
    assert msa.PAUSED == 'PAUSE'
