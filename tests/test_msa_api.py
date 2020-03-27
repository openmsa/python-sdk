"""
Test MSA API
"""

import datetime
import json
import os
from unittest.mock import patch

import pytest

from msa_sdk.msa_api import MSA_API


@pytest.fixture
def api_fixture(tmpdir):
    """
    API Fixtures
    """

    f_name = tmpdir.mkdir('test').join('vars_ctx_file')
    api_info = 'OTHER_VALUE-1=foobar-1\n'
    api_info += 'UBI_WILDFLY_JNDI_ADDRESS=test_hostname\n'
    api_info += 'UBI_WILDFLY_JNDI_PORT=1111\n'
    api_info += 'OTHER_VALUE-2=foobar-2\n'
    api_info += 'OTHER_VALUE-4=foobar-3\n'
    api_info += 'OTHER_VALUE-5=foobar-4\n'
    api_info += 'OTHER_VALUE-6=foobar-5\n'

    with open(f_name, 'w+') as t_file:
        t_file.write(api_info)

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        with patch('msa_sdk.constants.VARS_CTX_FILE', f_name):
            api = MSA_API()

    return api


@pytest.fixture
def environment_variable_fixture():
    """
    Fixture to test environment variables for API endpoint
    """
    os.environ['MSA_SDK_API_HOSTNAME'] = "environ_hostname"
    os.environ['MSA_SDK_API_PORT'] = "2222"

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        api = MSA_API()
    return api


@pytest.fixture
def default_hostname_fixture():
    """
    Fixure to use default hostname and port for API endpoint
    """
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'token': '12345qwert'}
        api = MSA_API()
    return api

# pylint: disable=redefined-outer-name


def test_read_hostname_json(api_fixture):
    """
    Test read hostname from json
    """
    api = api_fixture
    assert api.url == 'http://test_hostname:1111/ubi-api-rest'

# pylint: disable=redefined-outer-name


def test_environment_variable_hostname_json(environment_variable_fixture):
    """
    Test read hostname from json
    """
    api = environment_variable_fixture
    assert api.url == 'http://environ_hostname:2222/ubi-api-rest'
    del os.environ['MSA_SDK_API_HOSTNAME']
    del os.environ['MSA_SDK_API_PORT']

# pylint: disable=redefined-outer-name


def test_default_hostname_fixture(default_hostname_fixture):
    """
    Test read hostname from json
    """
    api = default_hostname_fixture
    assert api.url == 'http://localhost:8480/ubi-api-rest'


# pylint: disable=redefined-outer-name
def test_get_token(api_fixture):
    """
    Test Get Token
    """
    api = api_fixture

    assert api.token == '12345qwert'


# pylint: disable=redefined-outer-name
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

    assert api.process_content(
        'ENDED', 'Task OK', {
            "SERVICEINSTANCEID": "1234",
            "Other": "Value"}) == json.dumps(response)


# pylint: disable=redefined-outer-name
def test_content_with_log(api_fixture, tmpdir):
    """
    Test content with log
    """

    temp_dir = tmpdir.mkdir('with_log')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params
        }

        assert api.process_content('ENDED', 'Task OK', params,
                                   True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg = '\n=== {} ===\n{}'.format(log_time, json.dumps(params,
                                                                 indent=4))

        assert log_msg == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()


# pylint: disable=redefined-outer-name
def test_content_with_log_more_lines(api_fixture, tmpdir):
    """
    Test content with log with more lines
    """

    temp_dir = tmpdir.mkdir('with_log_more_lines')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params1 = {"SERVICEINSTANCEID": 1234, "Other": "Value1"}
        params2 = {"SERVICEINSTANCEID": 1234, "Other": "Value2"}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params1
        }

        assert api.process_content('ENDED', 'Task OK', params1,
                                   True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg_1 = '\n=== {} ===\n{}'.format(log_time, json.dumps(params1,
                                                                   indent=4))

        assert log_msg_1 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()

        api.process_content('ENDED', 'Task OK', params2, True)

        log_msg_2 = '{}\n=== {} ===\n{}'.format(
            log_msg_1, log_time, json.dumps(params2, indent=4))

        assert log_msg_2 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()


# pylint: disable=redefined-outer-name
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
