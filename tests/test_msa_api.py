"""
Test MSA API
"""

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
        with patch('sys.argv', ['--execute', 'path']):
            import msa_sdk
            api = api_fixture

            params = {
                "SERVICEINSTANCEID": 1234, "Other": "Value",
                "PROCESSINSTANCEID": 2345
            }

            response = {
                "wo_status": 'ENDED',
                "wo_comment": 'Task OK',
                "wo_newparams": params
            }

            assert api.process_content('ENDED', 'Task OK', params,
                                   True) == json.dumps(response)

        

# pylint: disable=redefined-outer-name
def test_content_with_log_more_lines(api_fixture, tmpdir):
    """
    Test content with log with more lines
    """

    temp_dir = tmpdir.mkdir('with_log_more_lines')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        api = api_fixture

        params1 = {
            "SERVICEINSTANCEID": 1234,
            "Other": "Value1",
            "PROCESSINSTANCEID": 2345}
        params2 = {
            "SERVICEINSTANCEID": 1234,
            "Other": "Value2",
            "PROCESSINSTANCEID": 3456}

        response = {
            "wo_status": 'ENDED',
            "wo_comment": 'Task OK',
            "wo_newparams": params1
        }

        assert api.process_content('ENDED', 'Task OK', params1,
                                   True) == json.dumps(response)

def test_log_to_process_file_success(api_fixture, tmpdir):
    """
    Test if log to process file is success

    it doesnn't works, because __init__ is called before everythings.
    """

    temp_dir = tmpdir.mkdir('log_to_process_file_success')
    f_path = '{}/{}'.format(temp_dir, "ctx.json")
    f_content ='''{
        "service_id": "12345",
        "TRACEID": "3629dd069a24067f",
        "SPANID": "9fa6859d92773b66",
        "TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJuY3Jvb3QiLCJpYXQiOjE2OTM0NzM0NjMsImx2bCI6IjEiLCJleHAiOjE3MDY0MzM0NjN9.0KYyakHt8-nyGm8wFKdyipH1ypTdn8Yn7A2YJYqUAyKRGjFH-7IlhfR2knlisDIXwRd3zbaST3bMcpCNsUssrg"
}'''
    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):
        with patch('sys.argv', ['prog', '--execute', f_path]):
            api = api_fixture

            params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

            log_message = 'Lorem ipsum dolor sit amet'

            assert api.log_to_process_file(
                params['SERVICEINSTANCEID'], log_message)


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

def test_task_pause(api_fixture, capsys):
    msa = api_fixture

    with pytest.raises(SystemExit) as sys_exit:
        msa.task_pause("Task pause", {'SERVICEINSTANCEID': 1}, False)

    captured = capsys.readouterr()
    output = (
        '{"wo_status": "PAUSE", "wo_comment": "Task pause",'
        ' "wo_newparams": {"SERVICEINSTANCEID": 1}}\n'
    )
    assert captured.out == output
    assert json.loads(captured.out)['wo_comment'] == 'Task pause'
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0
