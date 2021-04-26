"""Test util."""

import datetime
import io
import re
from unittest.mock import patch

from msa_sdk.util import address_is_in_network
from msa_sdk.util import cidr_match
from msa_sdk.util import cidr_to_range
from msa_sdk.util import cidr_to_subnet_and_subnetmask_address
from msa_sdk.util import convert_yang_into_xml_file
from msa_sdk.util import get_ip_range
from msa_sdk.util import get_vars_value
from msa_sdk.util import is_cidr
from msa_sdk.util import is_overlapping_cidr
from msa_sdk.util import log_to_process_file
from msa_sdk.util import netmask_to_cidr
from msa_sdk.util import obtain_file_lock
from msa_sdk.util import release_file_lock
from msa_sdk.util import update_asynchronous_task_details


def test_convert_yang_into_xml_file():
    """
    Test convert_yang_into_xml_file
    """

    assert convert_yang_into_xml_file(
        ['tests/test_yangconvertfile.yang'],
        'test_yangconvertfile.xml') == 'test_yangconvertfile.xml'

    fail_output = (
        'Error:Command \' cd "";  pyang -f sample-xml-skeleton '
        '--sample-xml-skeleton-doctype=config  '
        '-o test_yangconvertfile.xml test_yangconvertfile.yang\' '
        'returned non-zero exit status 1.'
    )

    assert convert_yang_into_xml_file(
        ['test_yangconvertfile.yang'],
        'test_yangconvertfile.xml') == fail_output


def test_get_ip_range():
    """
    Test get ip range
    """

    result = ['1.1.1.1', '1.1.1.2', '1.1.1.3', '1.1.1.4']

    assert get_ip_range('1.1.1.1', '1.1.1.4') == result

    result = ['10.3.1.253', '10.3.1.254', '10.3.1.255', '10.3.2.0', '10.3.2.1']

    assert get_ip_range('10.3.1.253', '10.3.2.1') == result


def test_cidr_to_range():
    """
    Test cidr range
    """
    result = ['10.3.1.{}'.format(x) for x in range(1, 255)]

    assert cidr_to_range('10.3.1.0/24') == result


def test_get_vars_value(tmpdir):
    """
    Test get vars value
    """

    f_content = (
        'DEVICE_INDEXATION_CRON_EXPR=0 0/5 * * *\n'
        'DISABLE_HTTPS_SERVER=&map|fr|false|en|false|ubi_en|false\n'
        'DISABLE_HTTPS_en=false\n'
        'DISABLE_HTTPS_fr=false\n'
        'DISABLE_HTTPS_ubi_en=false\n'
        'VAR1=test_var'
    )

    f_name = tmpdir.mkdir('get_vars_value').join('testfile')
    with open(f_name, 'w+') as t_file:
        t_file.write(f_content)
        t_file.close()

    with patch('msa_sdk.util.constants.VARS_CTX_FILE', f_name):
        assert get_vars_value('VAR1') == 'test_var'
        assert not get_vars_value('VARX')


def test_address_is_in_network():
    """
    Test address is in network
    """

    assert address_is_in_network('10.1.0.20', '10.1.0.0/24')
    assert not address_is_in_network('10.1.0.20', '10.0.0.0/24')


def test_is_cidr():
    """
    Test is cidr
    """

    assert is_cidr('10.1.1.2')


def test_not_cidr():
    """
    Test not cidr
    """

    assert not is_cidr('102.20.1.')


def test_netmask_to_cidr():
    """
    Test netmask to cidr
    """

    assert netmask_to_cidr('255.255.255.0') == 24


def test_is_overlapping_cidr():
    """
    Test is overlapping cidr
    """
    assert is_overlapping_cidr('10.0.0.0/16', '10.0.0.0/32')
    assert not is_overlapping_cidr('10.1.0.0/16', '10.0.0.0/32')


def test_cidr_match():
    """
    Test cidr_match
    """
    assert not cidr_match('10.1.0.20', '10.1.0.0/32')


def test_cidr_not_match():
    """
    Test cidr_match
    """
    assert not cidr_match('10.2.0.20', '10.1.0.0/32')


def test_cidr_to_subnet_and_netmask():
    """
    Test cidr to subnet and netmask
    """
    assert cidr_to_subnet_and_subnetmask_address('10.0.0.0/24') == \
        {'subnet_ip': '10.0.0.0', 'subnet_mask': '255.255.255.0'}

    assert cidr_to_subnet_and_subnetmask_address('10.0.0.0/16') == \
        {'subnet_ip': '10.0.0.0', 'subnet_mask': '255.255.0.0'}


def test_obtain_file_lock_no_previous_file(tmpdir):
    """
    Test obtain file lock when there is no previous file
    """
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    result = '{"wo_status": "ENDED", '
    result += '"wo_comment": "Lock obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+',
                {"SERVICEINSTANCEID": "12345", "process": "abc"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg


def test_obtain_file_lock_when_unlocked(tmpdir):
    """
    Test obtain file lock when the file is unlocked
    """
    f_content = 'unlocked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "ENDED", '
    result += '"wo_comment": "Lock obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+',
                {"SERVICEINSTANCEID": "12345", "process": "abc"},
                1, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg


def test_obtain_file_lock_when_locked(tmpdir):
    """
    Test obtain file lock when the file is locked
    """
    f_content = 'locked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "FAIL", '
    result += '"wo_comment": '
    result += '"Lock could not be obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12346", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.fcntl.flock') as mock_flock:
            mock_flock.side_effect = io.BlockingIOError()
            with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY',
                       f_dir_log):
                assert obtain_file_lock(
                    f_name, 'w+', {"SERVICEINSTANCEID": "12346",
                                   "process": "abc"}, 0.5, 2) == result

    log_file = '{}/process-12346.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12346",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg


def test_obtain_file_lock_content(tmpdir):
    """
    Test obtain file lock based on the content
    """

    f_content = 'locked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "FAIL", '
    result += '"wo_comment": '
    result += '"Lock could not be obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+', {"SERVICEINSTANCEID": "12345", "process": "abc"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg

    f_content = 'Unlocked'
    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "ENDED", '
    result += '"wo_comment": "Lock obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12346", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+', {"SERVICEINSTANCEID": "12346", "process": "abc"},
                0.5, 2) == result

    log_file = '{}/process-12346.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12346",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg


def test_release_file_lock(tmpdir):
    """
    Test release file lock
    """

    f_content = 'Locked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "ENDED", '
    result += '"wo_comment": '
    result += '"Lock released on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert release_file_lock(
                f_name, {"SERVICEINSTANCEID": "12345", "process": "abc"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg

    with open(f_path) as f_file:
        assert f_file.read().lower() == 'unlocked'


def test_release_file_lock_failed(tmpdir):
    """
    Test failed to release lock
    """

    f_content = 'Locked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_file_lock')
    f_dir_log = tmpdir.mkdir('obtain_file_lock_log')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "FAIL", '
    result += '"wo_comment": '
    result += '"Lock could not be released on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            with patch('msa_sdk.util.fcntl.flock') as mock_flock:
                mock_flock.side_effect = io.BlockingIOError
                assert release_file_lock(
                    f_name, {"SERVICEINSTANCEID": "12345", "process": "abc"},
                    0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===\n{}'.format(
        log_time,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc"\n}')
    )

    assert open(log_file).read() == log_msg

    with open(f_path) as f_file:
        assert f_file.read().lower() == 'locked'


def test_log_to_process_file_success(tmpdir):
    """
    Test if log to process file is success
    """

    temp_dir = tmpdir.mkdir('log_to_process_file_success')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        log_message = 'Lorem ipsum dolor sit amet'

        assert log_to_process_file(params['SERVICEINSTANCEID'], log_message)

        check_pattern = f'^.+?:DEBUG:{log_message}$'
        with open(f'{temp_dir}/process-1234.log', 'r') as log_file:
            assert re.match(check_pattern, log_file.read())


def test_log_to_process_file_fail():
    """
    Test if log to process file is fail due IOError
    """

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', '/loprem/'):

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value"}

        log_message = 'Lorem ipsum dolor sit amet'

        assert not log_to_process_file(params['SERVICEINSTANCEID'],
                                       log_message)


def test_update_asynchronous_task_details():
    """Test update asyncronous task"""

    with patch('msa_sdk.variables.Variables.task_call') as mock_task_call:
        with patch('requests.put') as mock_call_put:
            context = {
                "PROCESSINSTANCEID": 12,
                "TASKID": 13,
                "EXECNUMBER": 21,
                "TOKEN": "TOKEN1"
            }
            mock_task_call.return_value = context
            orch = update_asynchronous_task_details("details")

            mock_call_put.assert_called_once()
            assert orch.path == ('/orchestration/process/instance/12/task/'
                                 '13/execnumber/21/update')


def test_convert_yang_into_xml_file_error(tmpdir):
    f_dir = tmpdir.mkdir('yang2xml')
    f_input = f"{f_dir}/sample.yang"
    f_output = f"{f_dir}/sample.yang.to.xml"

    f_content_in = "invalid yang"

    with open(f_input, "w+") as f:
        f.write(f_content_in)

    yang_filenames = [f_input]
    xml_output_file = f_output
    ret = convert_yang_into_xml_file(yang_filenames, xml_output_file)

    assert re.match(r'^Error:', ret)


def test_convert_yang_into_xml_file_success(tmpdir):
    f_dir = tmpdir.mkdir('yang2xml')
    f_input = f"{f_dir}/sample.yang"
    f_output = f"{f_dir}/sample.yang.to.xml"

    f_content_in = """
    module sample {
      namespace "http://ubiqube.com/sample";
      prefix "spl";
      leaf greeting {
        type string;
        default "Hello world!";
      }
    }
    """
    f_content_out = """
    <?xml version='1.0' encoding='UTF-8'?>
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>
    """.replace("    ", "")[1:]

    with open(f_input, "w+") as f:
        f.write(f_content_in)

    yang_filenames = [f_input]
    xml_output_file = f_output
    convert_yang_into_xml_file(yang_filenames, xml_output_file)

    with open(f_output) as f:
        assert f.read() == f_content_out
