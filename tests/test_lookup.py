"""Module Test lookup."""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

from msa_sdk.lookup import Lookup
from util import _is_valid_json


@patch('requests.post')
def test_device_ids(mock_post):
    """Test a list of devices"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_dev = {
        'id': 71655,
        'prefix': 'hto',
        'ubiId': 'hto71655',
        'externalReference': 'hto71655'
    }

    second_dev = {
        'id': 73055,
        'prefix': 'CKB',
        'ubiId': 'CKB73055',
        'externalReference': 'CKB73055'
    }

    devices = [first_dev, second_dev]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(devices)

        lookup = Lookup()
        lookup.look_list_device_ids()

        assert lookup.path == '/lookup/devices'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content)[0] == first_dev
        assert json.loads(lookup.content)[1] == second_dev


@patch('requests.post')
def test_device_ids_fail(mock_post):
    """Test fail device ids"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get device ids",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')

        lookup = Lookup()
        lookup.look_list_device_ids()

        assert lookup.path == '/lookup/devices'
        assert lookup.content == json.dumps(fail_response)


@patch('requests.post')
def test_customer_ids(mock_post):
    """Test a list of customers"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_costu = {
        'id': 7117,
        'prefix': 'MSK',
        'ubiId': 'MSKA7117',
        'name': 'Training',
        'externalReference': 'MSKA7117',
        'operatorId': 3,
        'displayName': 'Training - MSKA7117',
        'displayNameForJsps': 'Training - MSKA7117',
        'type': 'A'
    }

    second_costu = {
        'id': 3158,
        'prefix': 'MSA',
        'ubiId': 'MSAA3158',
        'name': 'UBIqube demo',
        'externalReference': 'MSAA3158',
        'operatorId': 10,
        'displayName': 'UBIqube demo - MSAA3158',
        'displayNameForJsps': 'UBIqube demo - MSAA3158',
        'type': 'A'
    }

    customers = [first_costu, second_costu]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(customers)

        lookup = Lookup()
        lookup.look_list_customer_ids()

        assert lookup.path == '/lookup/customers'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content)[0] == first_costu
        assert json.loads(lookup.content)[1] == second_costu


@patch('requests.post')
def test_manager_ids(mock_post):
    """Test a list of managers"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_manager = {
        'id': 39311,
        'prefix': 'DGT',
        'ubiId': 'DGTG39311',
        'name': 'mnDelegation_Test',
        'externalReference': 'MDGT',
        'operatorId': 418,
        'displayName': 'mnDelegation_Test - MDGT',
        'displayNameForJsps': 'mnDelegation_Test - MDGT',
        'type': 'G'
    }

    second_manager = {
        'id': 39331,
        'prefix': 'RMG',
        'ubiId': 'RMGG39331',
        'name': 'mnDlg_TestRMG',
        'externalReference': 'MRMG',
        'operatorId': 420,
        'displayName': 'mnDlg_TestRMG - MRMG',
        'displayNameForJsps': 'mnDlg_TestRMG - MRMG',
        'type': 'G'
    }

    managers = [first_manager, second_manager]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(managers)

        lookup = Lookup()
        lookup.look_list_manager_ids()

        assert lookup.path == '/lookup/managers'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content) == managers


@patch('requests.post')
def test_manager_ids_fail(mock_post):
    """Test fail manager ids """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get manager ids",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')

        lookup = Lookup()
        lookup.look_list_manager_ids()

        assert lookup.path == '/lookup/managers'
        assert _is_valid_json(lookup.content)
        assert lookup.content == json.dumps(fail_response)


@patch('requests.post')
def test_operator_ids(mock_post):
    """Test a list of operator"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_operator = {
        'id': 39311,
        'prefix': 'DGT',
        'ubiId': 'DGTG39311',
        'name': 'mnDelegation_Test',
        'externalReference': 'MDGT',
        'operatorId': 418,
        'displayName': 'mnDelegation_Test - MDGT',
        'displayNameForJsps': 'mnDelegation_Test - MDGT',
        'type': 'G'
    }

    second_operator = {
        'id': 39331,
        'prefix': 'RMG',
        'ubiId': 'RMGG39331',
        'name': 'mnDlg_TestRMG',
        'externalReference': 'MRMG',
        'operatorId': 420,
        'displayName': 'mnDlg_TestRMG - MRMG',
        'displayNameForJsps': 'mnDlg_TestRMG - MRMG',
        'type': 'G'
    }

    operators = [first_operator, second_operator]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(operators)

        lookup = Lookup()
        lookup.look_list_operators_id(1234)

        assert lookup.path == '/lookup/operators/id/1234'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content) == operators


@patch('requests.post')
def test_operator_ids_fail(mock_post):
    """Test fail operator ids """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get operators id",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')

        lookup = Lookup()
        lookup.look_list_operators_id(1234)

        assert lookup.path == '/lookup/operators/id/1234'
        assert _is_valid_json(lookup.content)
        assert lookup.content == json.dumps(fail_response)


@patch('requests.post')
def test_sec_nodes(mock_post):
    """Test a list of sec nodes"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_sec_node = {
        'name': 'DEV-MA2',
        'logAddress': '10.30.18.86',
        'smsAddress': '127.0.0.1',
        'repNodeName': '',
        'isAlive': True,
        'ipv6Addr': '',
        'ipv6Mask': '64',
        'ipv6Gw': ''
    }

    sec_nodes = [first_sec_node]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(sec_nodes)

        lookup = Lookup()
        lookup.look_list_sec_nodes()

        assert lookup.path == '/lookup/sec_nodes'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content)[0] == first_sec_node


@patch('requests.post')
def test_sec_nodes_fail(mock_post):
    """Test fail sec nodes """

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get sec nodes",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')

        lookup = Lookup()
        lookup.look_list_sec_nodes()

        assert lookup.path == '/lookup/sec_nodes'
        assert _is_valid_json(lookup.content)
        assert lookup.content == json.dumps(fail_response)


@patch('requests.post')
def test_device_by_customer(mock_post):
    """Test list of device by customer ref"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    first_dev = {
        'id': 71655,
        'prefix': 'hto',
        'ubiId': 'hto71655',
        'externalReference': 'hto71655'
    }

    second_dev = {
        'id': 73055,
        'prefix': 'CKB',
        'ubiId': 'CKB73055',
        'externalReference': 'CKB73055'
    }

    devices = [first_dev, second_dev]

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.content = json.dumps(devices)

        lookup = Lookup()
        lookup.look_list_device_by_customer_ref('cust_ref')

        assert lookup.path == '/lookup/customer/devices/reference/cust_ref'
        assert _is_valid_json(lookup.content)

        assert json.loads(lookup.content) == devices


@patch('requests.post')
def test_device_by_customer_fail(mock_post):
    """Test fail list of device by customer ref"""

    mock_post.return_value.json.return_value = {'token': '12345qwert'}

    fail_response = {
        'wo_status': 'FAIL',
        'wo_comment': "Get list device by customer reference",
        'wo_newparams': "Not found"
    }

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value = MagicMock(ok=False, reason='Not found')

        lookup = Lookup()
        lookup.look_list_device_by_customer_ref('cust_ref')

        assert lookup.path == '/lookup/customer/devices/reference/cust_ref'
        assert lookup.content == json.dumps(fail_response)
