"""Test util."""

import datetime
import io
import re
from unittest.mock import patch

import msa_sdk
from msa_sdk.util import *


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
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+',
                {"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
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
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+',
                {"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},
                1, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
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
    result += '{"SERVICEINSTANCEID": "12346", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.fcntl.flock') as mock_flock:
            mock_flock.side_effect = io.BlockingIOError()
            with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY',
                       f_dir_log):
                assert obtain_file_lock(
                    f_name, 'w+', {"SERVICEINSTANCEID": "12346",
                                   "process": "abc", "PROCESSINSTANCEID": "2345"}, 0.5, 2) == result

    log_file = '{}/process-12346.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12346",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
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
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+', {"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345

    )

    assert open(log_file).read() == log_msg

    f_content = 'Unlocked'
    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = '{"wo_status": "ENDED", '
    result += '"wo_comment": "Lock obtained on the file {}",'.format(f_name)
    result += ' "wo_newparams": '
    result += '{"SERVICEINSTANCEID": "12346", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert obtain_file_lock(
                f_name, 'w+', {"SERVICEINSTANCEID": "12346", "process": "abc", "PROCESSINSTANCEID": "2345"},
                0.5, 2) == result

    log_file = '{}/process-12346.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12346",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
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
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert release_file_lock(
                f_name, {"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},
                0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
    )

    assert open(log_file).read() == log_msg

    with open(f_path) as f_file:
        assert f_file.read().lower() == 'unlocked'


def test_obtain_file_lock_exclusif_no_previous_file(tmpdir):
    """Test obtain_file_lock_exclusif"""

    f_content = 'Locked by TRRR with serviceinstancereference='
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    if os.path.exists(f_path):
      os.remove(f_path)    

    result = 'Lock obtained on the file lockfile, full_path='+f_path
    with patch('msa_sdk.variables.Variables.task_call') as mock_task_call:
      with patch('requests.put') as mock_call_put:
        context = {
            "PROCESSINSTANCEID": 12,
            "SERVICEINSTANCEID": 21,
            "UBIQUBEID": "INF152",
            "SERVICEINSTANCEREFERENCE":"INF152"
        }
        mock_task_call.return_value = context
        with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
            with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
                assert result in obtain_file_lock_exclusif(
                    f_name, {"UBIQUBEID":"INF152"},'w+', 2, 10)

def test_obtain_file_lock_exclusif_with_previous_file_OK(tmpdir):
    """Test obtain_file_lock_exclusif"""

    f_content = 'Locked by INF152 with serviceinstancereference=INF1252 on '
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
         f_file.write(f_content)

    result = 'Lock obtained on the file lockfile, full_path='

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert result in obtain_file_lock_exclusif(
                f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},'w+', 2, 10)

def test_obtain_file_lock_exclusif_with_previous_file_unlock_OK(tmpdir):
    """Test obtain_file_lock_exclusif"""

    f_content = 'unlocked'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
         f_file.write(f_content)

    result = 'Lock obtained on the file lockfile, full_path='

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert result in obtain_file_lock_exclusif(
                f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},'w+', 2, 10)


def test_obtain_file_lock_exclusif_previous_file_failed(tmpdir):
    """Test obtain_file_lock_exclusif"""

    f_content = 'Locked by TEST with serviceinstancereference='
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'After waiting 20 secondes, lock could not be obtained on the file lockfile'

    with patch('msa_sdk.variables.Variables.task_call') as mock_task_call:
      with patch('requests.put') as mock_call_put:
        context = {
            "PROCESSINSTANCEID": 12,
            "SERVICEINSTANCEID": 21,
            "UBIQUBEID": "INF152",
            "TASKID": "2544",
            "SERVICEINSTANCEREFERENCE":"INF152",
            "EXECNUMBER": 225,
            "TOKEN": 'TUFUFU'
        }
        mock_task_call.return_value = context
        with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
            with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
                assert result in obtain_file_lock_exclusif(
                    f_name, {"UBIQUBEID":"INF152"},'w+', 2, 10)

def test_obtain_file_lock_exclusif_previous_file_unlock_failed(tmpdir):
    """Test obtain_file_lock_exclusif"""

    f_content = 'unlock'
    f_name    = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'After waiting 20 secondes, lock could not be obtained on the file lockfile'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            with patch('msa_sdk.util.fcntl.flock') as mock_flock:
                mock_flock.side_effect = io.BlockingIOError
                assert result in obtain_file_lock_exclusif(f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},'w+', 2, 10)

           
def test_obtain_file_lock_exclusif_bad_file_failed(tmpdir):
    """Test obtain_file_lock_exclusif  should not be eable to write file"""

    f_content = 'RRLocked for test'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'After waiting 20 secondes, lock could not be obtained on the file lockfile'
    f_dir = '/rootTEST2'
    # f_dir_log = '/TESTlog'
    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            with patch('msa_sdk.util.fcntl.flock') as mock_flock:
                mock_flock.side_effect = io.BlockingIOError
                assert result in obtain_file_lock_exclusif(f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},'w+', 2, 10)
           
           
def test_release_file_lock_exclusif(tmpdir):
    """
    Test release file lock exclusif
    """

    f_content = 'Locked by INF152 with serviceinstancereference=INF1252 on '

    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'Lock released on the file lockfile, full_path='

    with patch('msa_sdk.variables.Variables.task_call') as mock_task_call:
      with patch('requests.put') as mock_call_put:
        context = {
            "PROCESSINSTANCEID": 12,
            "SERVICEINSTANCEID": 21,
            "UBIQUBEID": "INF152",
            "TASKID": "2544",
            "SERVICEINSTANCEREFERENCE":"INF1252",
            "EXECNUMBER": 225,
            "TOKEN": 'TUFUFU'
        }
        mock_task_call.return_value = context
        with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
            with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
                assert result in release_file_lock_exclusif(
                    f_name, {"UBIQUBEID":"INF152"}, 2, 10)


def test_release_file_lock_exclusif_failed(tmpdir):
    """
    Test release file lock exclusif
    """

    f_content = 'TEST lock file'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'After waiting 20 secondes, lock could not be released '

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert result in  release_file_lock_exclusif(
                f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}, 2, 10)

def test_release_file_lock_exclusif_locked_by_failed(tmpdir):
    """
    Test release file lock exclusif
    """

    f_content = 'locked by TEST'
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    with open(f_path, 'w+') as f_file:
        f_file.write(f_content)

    result = 'After waiting 20 secondes, lock could not be released '

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert result in  release_file_lock_exclusif(
                f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}, 2, 10)

def test_release_file_lock_exclusif_no_previous_lock(tmpdir):
    """
    Test release file lock exclusif
    """

    f_content = 'Locked by  with serviceinstancereference='
    f_name = 'lockfile'

    f_dir = tmpdir.mkdir('obtain_exclusif')
    f_dir_log = tmpdir.mkdir('obtain_log_exclusif')

    f_path = '{}/{}'.format(f_dir, f_name)

    if os.path.exists(f_path):
      os.remove(f_path) 

    result = 'Lock file not exist ('

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            assert result in  release_file_lock_exclusif(
                f_name, {"UBIQUBEID":"INF152", "SERVICEINSTANCEREFERENCE":"INF1252", "SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}, 2, 10)

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
    result += '{"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"}'
    result += '}'

    with patch('msa_sdk.util.constants.UBI_JENTREPRISE_DIRECTORY', f_dir):
        with patch('msa_sdk.util.constants.PROCESS_LOGS_DIRECTORY', f_dir_log):
            with patch('msa_sdk.util.fcntl.flock') as mock_flock:
                mock_flock.side_effect = io.BlockingIOError
                assert release_file_lock(
                    f_name, {"SERVICEINSTANCEID": "12345", "process": "abc", "PROCESSINSTANCEID": "2345"},
                    0.5, 2) == result

    log_file = '{}/process-12345.log'.format(f_dir_log)

    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = '\n=== {} ===|{}|\n{}\n=== {} ===|{}--|'.format(
        log_time, 2345,
        ('{\n    "SERVICEINSTANCEID": "12345",'
         '\n    "process": "abc",'
         '\n    "PROCESSINSTANCEID": "2345"\n}'), log_time, 2345
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

def test_log_to_service_file_success(tmpdir):
    """
    Test if log to process file is success
    """

    temp_dir = tmpdir.mkdir('log_to_process_file_success')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value", "PROCESSINSTANCEID": 2345}

        log_message = 'Lorem ipsum dolor sit amet'

        assert log_to_process_file(params['SERVICEINSTANCEID'], log_message, params['PROCESSINSTANCEID'])

        check_pattern = r'^\n.+?|2345|\n{log_message}$'
        with open(f'{temp_dir}/process-1234.log', 'r') as log_file:
            assert re.match(check_pattern, log_file.read())

def test_log_line_break_to_service_file_success(tmpdir):
    """
    Test if log to process file is success
    """

    temp_dir = tmpdir.mkdir('log_to_process_file_success')

    with patch('msa_sdk.constants.PROCESS_LOGS_DIRECTORY', temp_dir):

        params = {"SERVICEINSTANCEID": 1234, "Other": "Value", "PROCESSINSTANCEID": 2345}

        log_message = 'Lorem ipsum dolor sit amet\ntest'

        assert log_to_process_file(params['SERVICEINSTANCEID'], log_message, params['PROCESSINSTANCEID'])

        check_pattern = r'^\n.+?|2345|{log_message}$\n^.+?|2345--|'
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
