"""Module util."""
import fcntl
import io
import os
import time
from configparser import ConfigParser
from ipaddress import AddressValueError
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from ipaddress import ip_network

from msa_sdk import constants
from msa_sdk.msa_api import MSA_API


def get_ip_range(start, end):
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
    List of range of ips

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
    List of ip range

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
    Json

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
            tries += 1
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
    Json

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
            tries += 1
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
    Bool: Check if both cidr overlaps

    """
    return IPv4Network(cidr1).overlaps(IPv4Network(cidr2))


def get_vars_value(variable):
    """

    Get vars value.

    Parameters
    ----------
    variable: String
        Variables name

    Returns
    -------
    Value

    """
    config = ConfigParser()
    with open(constants.VARS_CTX_FILE, 'r') as f_file:
        config.read_string('[config]\n' + f_file.read())

    if not config.has_option('config', variable):
        return False

    vars_file = config.get('config', variable)

    return vars_file


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
    Bool

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
    Returns cdir

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

def log_to_process_file(process_id: str, log_message: str) -> bool:
        """
    
        Write log string with ISO timestamp to process log file.
    
        Parameters
        ----------
        process_id: String
                    Process ID of current process
        log_message: String
                     Log text
    
        Returns
        -------
        True:  log string has been written correctlly
        False: log string has not been written correctlly or the log file doesnt exist

        """
        import sys
        from datetime import datetime
        process_log_path = '{}/process-{}.log'.format(constants.PROCESS_LOGS_DIRECTORY,
                                                      process_id)
        current_time = datetime.now().isoformat()
        log_string = '{date}:{file}:DEBUG:{msg}\n'.format(date = current_time,
                                                          file = sys.argv[0].split('/')[-1],
                                                          msg = log_message)
        try:
            with open(process_log_path, 'a') as log_file:
                written_characters = log_file.write(log_string)
                return True
        except IOError:
            return False

