"""
Test MSA API
"""

import datetime
import json
import os
import re
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

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value", "PROCESSINSTANCEID": 2345}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params
        }

        assert api.process_content('ENDED', 'Task OK', params,
                                   True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(log_time, params['PROCESSINSTANCEID'], json.dumps(params,
                                                                 indent=4), log_time, params['PROCESSINSTANCEID'])

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

        params1 = {"SERVICEINSTANCEID": 1234, "Other": "Value1", "PROCESSINSTANCEID": 2345}
        params2 = {"SERVICEINSTANCEID": 1234, "Other": "Value2", "PROCESSINSTANCEID": 3456}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params1
        }

        assert api.process_content('ENDED', 'Task OK', params1,
                                   True) == json.dumps(response)

        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg_1 = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(log_time, params1['PROCESSINSTANCEID'], json.dumps(params1,
                                                                   indent=4), log_time, params1['PROCESSINSTANCEID'] )

        assert log_msg_1 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()

        api.process_content('ENDED', 'Task OK', params2, True)

        log_msg_2 = '{}\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
            log_msg_1, log_time, params2['PROCESSINSTANCEID'], json.dumps(params2, indent=4), log_time, params2['PROCESSINSTANCEID'])

        assert log_msg_2 == open(
            '{}/{}'.format(temp_dir, 'process-1234.log'), 'r').read()


def test_log_to_process_file_success(api_fixture, tmpdir):
    """
    Test if log to process file is success
    """

    temp_dir = tmpdir.mkdir('log_to_process_file_success')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        log_message = 'Lorem ipsum dolor sit amet'

        assert api.log_to_process_file(
            params['SERVICEINSTANCEID'], log_message)

        check_pattern = f'^.+?:DEBUG:{log_message}$'
        with open(f'{temp_dir}/process-1234.log', 'r') as log_file:
            assert re.match(check_pattern, log_file.read())


def test_log_to_process_file_fail(api_fixture, tmpdir):
    """
    Test if log to process file is fail due IOError
    """

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', '/loprem/'):
        api = api_fixture

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        log_message = 'Lorem ipsum dolor sit amet'

        assert not api.log_to_process_file(
            params['SERVICEINSTANCEID'],
            log_message)


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


def test_task_error(api_fixture, capsys):
    msa = api_fixture

    with pytest.raises(SystemExit) as sys_exit:
        msa.task_error("Task error", {'SERVICEINSTANCEID': 1}, False)

    captured = capsys.readouterr()
    output = (
        '{"wo_status": "FAIL", "wo_comment": "Task error",'
        ' "wo_newparams": {"SERVICEINSTANCEID": 1}}\n'
    )
    assert captured.out == output
    assert json.loads(captured.out)['wo_comment'] == 'Task error'
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1


def test_task_success(api_fixture, capsys):
    msa = api_fixture

    with pytest.raises(SystemExit) as sys_exit:
        msa.task_success("Task success", {'SERVICEINSTANCEID': 1}, False)

    captured = capsys.readouterr()
    output = (
        '{"wo_status": "ENDED", "wo_comment": "Task success",'
        ' "wo_newparams": {"SERVICEINSTANCEID": 1}}\n'
    )

    assert captured.out == output
    assert json.loads(captured.out)['wo_comment'] == 'Task success'

    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0
