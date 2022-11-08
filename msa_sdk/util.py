"""Module util."""
import fcntl
import io
import os
import subprocess
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from ipaddress import AddressValueError
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from ipaddress import ip_network

from msa_sdk import constants
from msa_sdk.orchestration import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk.variables import Variables


def convert_yang_into_xml_file(yang_filenames, xml_output_file: str):
    """
    Convert YANG files into one XML file.

    Parameters
    ----------
    yang_filenames: Array
            It contains the list of YANG files (with full path name of
            each files

    Returns
    -------
    xml_output_file: String
            Filename of the new YANG file

    """
    # Get the directory where all PYANG files are present. We should run
    # pyang in this directory to be able to load other yang generic library
    # dependency present in the same directory.
    yang_path = os.path.dirname(yang_filenames[0])
    yang_files = ''
    for file in yang_filenames:
        yang_files = yang_files + ' ' + str(os.path.basename(file))

    pyang_command = ' cd "' + yang_path + \
        '";  pyang -f sample-xml-skeleton ' + \
        '--sample-xml-skeleton-doctype=config  -o ' + \
        xml_output_file + yang_files

    try:
        subprocess.check_output(pyang_command, shell=True,
                                stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error_msg:
        return 'Error:' + str(error_msg)

    return xml_output_file


def get_ip_range(start, end) -> list:
    """

    Generate a list of all IP addresses between $start and $end (inclusive).

    For Ex. (1.1.1.1, 1.1.1.5) => [1.1.1.1, 1.1.1.2, 1.1.1.3, 1.1.1.4, 1.1.1.5]

    Parameters
    ----------
    start: String
            start of the range
    end: String
            end of the range

    Returns
    -------
    list: List of range of ips

    """
    ip_range = list(range(int(IPv4Address(start)), int(IPv4Address(end))))
    result = list(map(lambda x: str(IPv4Address(x)), ip_range))
    result.append(end)

    return result


def cidr_to_range(cdir):
    """

    Get the Start and End Address of the IP range from CIDR.

    Eg.[10.0.0.0/24] => 10.0.0.0 - 10.0.0.255

    Parameters
    ----------
    cdir: String
        cdir range

    Returns
    -------
    list: List of ip range

    """
    r_ips = list(ip_network(cdir).hosts())
    ip_range = [str(x) for x in r_ips]

    return ip_range


def obtain_file_lock(lock_file_name, mode, process_param, sleep_time=60,
                     timeout=300):
    """

    Obtain lock file.

    Parameters
    ----------
    lock_file_name: String
        File name
    mode: String mode
        File mode
    process_param: options PROCESSINSTANCEID, TASKID, EXECNUMBER
        Process parameters
    sleep_time: Integer
        Time to wait until next try
    timeout: Integer
        How much time (timeout * sleep_time) it will take to timeout

    Returns
    ------
    json: Result of the lock

    """
    lock_file_path = '{}/{}'.format(constants.UBI_JENTREPRISE_DIRECTORY,
                                    lock_file_name)

    lock_obtained = False

    r_json = ''
    tries = 1
    while not lock_obtained and tries < timeout:
        try:
            if os.path.exists(lock_file_path):
                with open(lock_file_path) as f_file:
                    file_content = f_file.read()
            else:
                f_lock_file = open(lock_file_path, mode)
                fcntl.flock(f_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with open(lock_file_path, 'w+') as f_file:
                    f_file.write('Locked')
                lock_obtained = True
                fcntl.flock(f_lock_file, fcntl.LOCK_UN)
                continue

            if 'unlocked' not in file_content.lower():
                raise io.BlockingIOError

            lock_obtained = True
        except io.BlockingIOError:
            tries += sleep_time
            time.sleep(sleep_time)

    if not lock_obtained:
        r_json = MSA_API.process_content(
            constants.FAILED,
            'Lock could not be obtained on the file {}'.format(
                lock_file_name),
            process_param,
            True)
    else:
        r_json = MSA_API.process_content(
            constants.ENDED,
            'Lock obtained on the file {}'.format(lock_file_name),
            process_param,
            True)

    return r_json


def release_file_lock(lock_file_name, process_param, sleep_time=60,
                      timeout=300):
    """

    Release lock file.

    Parameters
    ----------
    lock_file_name: String
        File name
    process_param: options PROCESSINSTANCEID, TASKID, EXECNUMBER
        Process parameters
    sleep_time: Integer
        Time to wait until next try
    timeout: Integer
        How much time (timeout * sleep_time) it will take to timeout

    Returns
    ------
    json: Result of the release

    """
    lock_file_path = '{}/{}'.format(constants.UBI_JENTREPRISE_DIRECTORY,
                                    lock_file_name)

    f_lock_file = open(lock_file_path)

    r_json = ''
    tries = 1

    while tries < timeout:
        try:
            fcntl.flock(f_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with open(lock_file_path, 'w+') as f_file:
                f_file.write('Unlocked')
            fcntl.flock(f_lock_file, fcntl.LOCK_UN)
            break

        except io.BlockingIOError:
            tries += sleep_time
            time.sleep(sleep_time)

    if tries >= timeout:
        r_json = MSA_API.process_content(
            constants.FAILED,
            'Lock could not be released on the file {}'.format(
                lock_file_name), process_param, True)
    else:
        r_json = MSA_API.process_content(
            constants.ENDED,
            'Lock released on the file {}'.format(lock_file_name),
            process_param, True)

    return r_json


def obtain_file_lock_exclusif(lock_file_name, process_param, mode= 'w+', sleep_time=15, max_try_nb=10):
    """

    Lock one file exclusivly (only the subtenant and instance_id who make the lock can unlock the file. If the file is locked by one other subtenant or instance_id, it will retry many time (<max_try_nb) to get the lock.

    Parameters
    ----------
    lock_file_name: String
        File name
    mode: String mode like 'w+'
        File mode
    process_param: options PROCESSINSTANCEID, TASKID, EXECNUMBER
        Process parameters
    sleep_time: Integer
        Time to wait until next try
    max_try_nb: Integer
        Max number of try, the timeout will be max_try_nb * sleep_time

    Returns
    ------
    Result of the lock

    """
    dev_var = Variables()
    context = Variables.task_call(dev_var)
    lock_file_path = '{}/{}'.format(constants.UBI_JENTREPRISE_DIRECTORY, lock_file_name)

    lock_obtained = False

    r_json = ''
    tries = 1
    if not process_param.get('UBIQUBEID') or not process_param.get('SERVICEINSTANCEREFERENCE'):
      process_param['UBIQUBEID'] = context['UBIQUBEID'] 
      process_param['SERVICEINSTANCEREFERENCE'] = context['SERVICEINSTANCEREFERENCE']
    lock_content = 'Locked by '+process_param['UBIQUBEID'] + ' with serviceinstancereference=' + process_param['SERVICEINSTANCEREFERENCE'] +' on '

      #lock_content = 'Locked by  with serviceinstancereference='
    if not process_param.get('SERVICEINSTANCEID'):
      process_param['SERVICEINSTANCEID'] = context['SERVICEINSTANCEID']
    if not process_param.get('PROCESSINSTANCEID'):
      process_param['PROCESSINSTANCEID'] = context['PROCESSINSTANCEID']      

    lock_content_lower = lock_content.lower()
    while not lock_obtained and tries < max_try_nb:
        wait_message = False
        try:
            file_content = ''
            if os.path.exists(lock_file_path):
              with open(lock_file_path) as f_file:
                file_content = f_file.read()
              file_content_lower = file_content.lower()  
              if lock_content_lower in file_content_lower:
                #wait_message = 'Lock file already done by this instance : ' + lock_content
                lock_obtained = True
                continue
              elif "locked by " in file_content_lower:
                wait_message = 'Wait, lock file already done by : ' + file_content
                raise FileNotFoundError
              elif "unlocked" in file_content_lower:
                os.remove(lock_file_path)
            else:
              day         = time.strftime("%Y/%m/%d %H:%M:%S")
              f_lock_file = open(lock_file_path, mode)
              fcntl.flock(f_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
              with open(lock_file_path, 'w+') as f_file:
                  f_file.write(lock_content + day)
              lock_obtained = True
              fcntl.flock(f_lock_file, fcntl.LOCK_UN)
              continue
        
        except FileNotFoundError:
          if wait_message:
            if context.get('UBIQUBEID'):
              update_asynchronous_task_details(wait_message)
            time.sleep(sleep_time)
        tries = tries + 1

    if not lock_obtained:
      nb_sec = max_try_nb * sleep_time 
      if wait_message: 
        r_json = MSA_API.process_content(constants.FAILED, 'After waiting '+str(nb_sec)+' secondes, lock could not be obtained on the file '+lock_file_name+' (full_path='+lock_file_path+') : '+ wait_message, process_param, True)
      else:
        r_json = MSA_API.process_content(constants.FAILED, 'After waiting '+str(nb_sec)+' secondes, lock could not be obtained on the file '+lock_file_name+', full_path='+lock_file_path, process_param, True)
    else:        
      r_json = MSA_API.process_content(constants.ENDED, 'Lock obtained on the file '+lock_file_name+', full_path='+lock_file_path, process_param, True)
    return r_json

def release_file_lock_exclusif(lock_file_name, process_param, sleep_time=30, max_try_nb = 10):
    """

    Release lock file exclusif (only the subtenant and instance_id who make the lock can unlock.

    Parameters
    ----------
    lock_file_name: String
        File name
    process_param: options PROCESSINSTANCEID, TASKID, EXECNUMBER
        Process parameters
    sleep_time: Integer
        Time to wait until next try
    max_try_nb: Integer
        Max number of try, the timeout will be max_try_nb * sleep_time


    Returns
    ------
    Result of the release

    """
    dev_var = Variables()
    context = Variables.task_call(dev_var)

    lock_file_path = '{}/{}'.format(constants.UBI_JENTREPRISE_DIRECTORY,
                                    lock_file_name)

    r_json = ''
    tries = 1
    if not process_param.get('UBIQUBEID') or not process_param.get('SERVICEINSTANCEREFERENCE'):
      process_param['UBIQUBEID'] = context['UBIQUBEID'] 
      process_param['SERVICEINSTANCEREFERENCE'] = context['SERVICEINSTANCEREFERENCE']
    lock_content = 'Locked by '+process_param['UBIQUBEID'] + ' with serviceinstancereference=' + process_param['SERVICEINSTANCEREFERENCE'] +' on '
    if not process_param.get('SERVICEINSTANCEID'):
      process_param['SERVICEINSTANCEID'] = context['SERVICEINSTANCEID']
    if not process_param.get('PROCESSINSTANCEID'):
      process_param['PROCESSINSTANCEID'] = context['PROCESSINSTANCEID']      
      
    release_obtained = False
    lock_content_lower = lock_content.lower()
    wait_message = 'Wait'
    message = 'Lock released on the file {}, full_path={}'.format(lock_file_name, lock_file_path)

    while not release_obtained and tries < max_try_nb:
        file_content_lower = ''
        if os.path.exists(lock_file_path):
          with open(lock_file_path) as f_file:
            file_content = f_file.read().lower()
            if lock_content_lower in file_content.lower():
              # Lock file already done by this instance, we can unlock it
              os.remove(lock_file_path)
              release_obtained = True
              continue
            elif "locked by" in file_content.lower():
              wait_message = 'Wait, lock file already done by : ' + file_content
          
          tries = tries + 1
          # if process_param['UBIQUBEID']:
            # update_asynchronous_task_details(wait_message)
          time.sleep(sleep_time)
        
        else:
          message = 'Lock file not exist ({}, full_path={}), it was already unlocked '.format(lock_file_name, lock_file_path)
          release_obtained = True
          continue
    if tries >= max_try_nb:
      nb_sec = max_try_nb * sleep_time 
      r_json = MSA_API.process_content(constants.FAILED,  'After waiting '+str(nb_sec)+' secondes, lock could not be released on the file '+lock_file_name+', full_path='+lock_file_path+ ' : '+wait_message, process_param, True)
    else:
      r_json = MSA_API.process_content(constants.ENDED,  message, process_param, True)

    return r_json


def is_overlapping_cidr(cidr1, cidr2):
    """

    Check if cidr1 overlaps cidr2.

    Parameters
    ---------
    cidr1: String
        First cidr to compare
    cidr2: String
        Second cidr to compare

    Returns
    -------
    bool: Cidr overlaps

    """
    return IPv4Network(cidr1).overlaps(IPv4Network(cidr2))


def address_is_in_network(addr, net):
    """

    Address is in network.

    Parameters
    ----------
    addr: String
        Address - 10.0.0.20
    net: String
        Network - 10.0.0.0/24
    mask: String
        Network mask

    Returns
    -------
    Bool - Returns if the address overlaps a network

    """
    return IPv4Network(addr).overlaps(IPv4Network(net))


def is_cidr(addr):
    """

    Check if a valid cidr.

    Parameters
    ----------
    addr: String
        IP address

    Returns
    -------
    bool: Valid cidr

    """
    try:
        IPv4Address(addr)
    except AddressValueError:
        return False

    return True


def netmask_to_cidr(netmask):
    """

    Netmask to cidr.

    Parameters
    ----------
    netmask: String
        Netmask

    Returns
    -------
    string: cidr netmask

    """
    return sum([bin(int(x)).count("1") for x in netmask.split(".")])


def cidr_match(ip_addr, cidr):
    """

    Match cidr.

    Parameters
    ----------
    ip_addr: String
        IP Address eg: 10.1.0.20
    cidr: String
        cidr eg. 10.1.0.20/32

    Returns
    -------
    Bool

    """
    subnet, mask = cidr.split('/')

    return (int(IPv4Address(ip_addr)) & ~((1 << (32 - int(mask))) - 1)) == \
        int(IPv4Address(subnet))


def cidr_to_subnet_and_subnetmask_address(cidr):
    """

    Get the subnet and subnetmast from a cidr.

    Parameters
    ----------
    cidr: String eg. '10.0.0.0/24'
        cidr value

    Returns
    -------
    Dict: netmask and network_address

    """
    network = IPv4Network(cidr)

    return {'subnet_ip': str(network.network_address),
            'subnet_mask': str(network.netmask)}


def log_to_process_file(service_id: str, log_message: str,
                        process_id: str = None) -> bool:
    """

    Write log string with ISO timestamp to process log file.

    Parameters
    ----------
    service_id: String
                Service ID of current process
    log_message: String
                 Log text
    process_id: String
                Process ID of current process

    Returns
    -------
    bool:
        true:  log string has been written correctlly

        false: log string has not been written correctlly or the
                log file doesnt exist

    """
    process_log_path = '{}/process-{}.log'.format(
        constants.PROCESS_LOGS_DIRECTORY, service_id)
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not process_id:
        log_string = '{date}:{file}:DEBUG:{msg}\n'.format(
            date=log_time, file=sys.argv[0].split('/')[-1], msg=log_message)
    else:
        log_string = '\n=== {} ===|{}|\n{}'.format(
            log_time, process_id, log_message)
        if "\n" in log_message:
            log_string += '\n=== {} ===|{}--|'.format(
                log_time, process_id)
    try:
        with open(process_log_path, 'a') as log_file:
            log_file.write(log_string)
    except IOError:
        return False

    return True

def log_to_process_file(context: dict, log_message: str) -> bool:
    """
    Write log string with ISO timestamp to process log file.

    Parameters
    ----------
    context: Dict
                Workflow context
    log_message: String
                 Log text

    Returns
    -------
    bool:
        true:  log string has been written correctlly

        false: log string has not been written correctlly or the
                log file doesnt exist

    """
    log_to_process_file(context.get('SERVICEINSTANCEID'), log_message, context.get('PROCESSINSTANCEID'))

def update_asynchronous_task_details(details: str):
    """

    Update Asynchronous Task details.

    Print task details during Process execution.

    Parameters
    ----------
    detail: String
            The message to display in msa-ui

    Returns
    -------
    object: Orchestration

    """
    context = Variables.task_call()
    process_instance_id = context['PROCESSINSTANCEID']
    task_id = context['TASKID']
    exec_number = context['EXECNUMBER']
    orch = Orchestration(None)
    orch.update_asynchronous_task_details(process_instance_id, task_id,
                                          exec_number, details)
    return orch
