"""
Test Orchestration
"""
from unittest.mock import patch

from util import _is_valid_json
from util import orchestration_fixture  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def test_list_service_instances(orchestration_fixture):
    """
    Test List Service Instances
    """

    device_info = (
        '[{"name":"Process/Reference/Customer/Kibana/kibana_dashboard",'
        '"id":2102,"serviceExternalReference":"MSASID2102","state":"ACTIVE"},'
        '{"name":"Process/Reference/Customer/Kibana/kibana_dashboard",'
        '"id":2258,"serviceExternalReference":"MSASID2258","state":"ACTIVE"},'
        '{"name":"Process/Reference/Customer/Kibana/kibana_dashboard",'
        '"id":2231,"serviceExternalReference":"MSASID2231","state":"ACTIVE"},'
        '{"name":"Process/Reference/Device_Management/Device_Management_List",'
        '"id":1536,"serviceExternalReference":"MSASID1536","state":"ACTIVE"}]')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.list_service_instances()
        assert orch.path == '/orchestration/MSAA19224/service/instance'
        assert _is_valid_json(orch.response.text)


def test_get_service_variables_by_service_id(orchestration_fixture):
    """
    Test Get Service variables by Service ID
    """
    device_info = ('[{"comment":"","name":"SERVICEINSTANCEID",'
                   '"value":"205710"},'
                   '{"comment":"","name":"service_id",'
                   '"value":"205710"}]')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.get_service_variables('1234')
        assert orch.path == '/orchestration/service/variables/1234'
        assert _is_valid_json(orch.response.text)


def test_get_list_service_by_status(orchestration_fixture):
    """
    Test Get list of services by status
    """
    response = (
        '{"Process/IP_CONTROLLER/Fulfilment_Dispatcher/Fulfilment_Dispatcher":'
        '{"RUNNING":0,"ENDED":0,"WARNING":0,"FAIL":0},"Process/IP_CONTROLLER/'
        'Fulfilment_Handler/Fulfilment_Handler":{"RUNNING":0,"ENDED":0,'
        '"WARNING":0,"FAIL":0}}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = response
        orch = orchestration_fixture
        orch.get_list_service_by_status(1)
        assert orch.path == '/orchestration/v1/services?ubiqubeId=MSAA19224&range=1'
        assert _is_valid_json(orch.response.text)


def test_get_service_status_by_id(orchestration_fixture):
    """
    Test Get service status by ID
    """
    import json
    response = (
        '[{"serviceId":{"name":"Process/IP_CONTROLLER/Cleaner/Cleaner","id":398,'
        '"serviceExternalReference":"FSTSID398","state":null},"processId":'
        '{"name":"Process/IP_CONTROLLER/Cleaner/Cleaner","id":448,"lastExecNumber":1,'
        '"submissionType":"RUN"},"status":{"status":"ENDED","details":"Cleanerhasbeenfinished",'
        '"startingDate":"2021-01-2911:33:23.865242","endingDate":"2021-01-2911:33:29.19334",'
        '"execNumber":1,"processTaskStatus":[{"status":"ENDED","order":1,"processInstanceId":448,'
        '"scriptName":"Cleaner","details":"Cleanerhasbeenfinished",'
        '"startingDate":"2021-01-2911:33:23.878261","endingDate":"2021-01-2911:33:29.19334",'
        '"newParameters":[]}]},"executorUsername":"ncroot"}]')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = response
        orch = orchestration_fixture
        assert orch.get_service_status_by_id(398) == 'ENDED'
        assert orch.path == '/orchestration/v1/service/process-instance/398'

    response_fail = ('[]')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = response_fail
        orch = orchestration_fixture
        assert orch.get_service_status_by_id(398) is None
        assert orch.path == '/orchestration/v1/service/process-instance/398'

def test_get_process_status_by_id(orchestration_fixture):
    """
    Test Get service status by ID
    """
    import json
    response = (
        '{ "serviceId": { "name": "Process/workflows/TestConPy/TestConPy", "id": 187201, '
        '"serviceExternalReference": "IOSSID187201", "state": null }, '
        '"processId": { "name": "Process/workflows/TestConPy/Process_Test", '
        '"id": 189406, "lastExecNumber": 1, "submissionType": "RUN" }, '
        '"status": { "status": "ENDED", "details": "Task OK", "startingDate": "2021-06-21 11:42:34.731975", '
        '"endingDate": "2021-06-21 11:42:35.108229", "execNumber": 1, "processReference": null, '
        '"processTaskStatus": [ { "status": "ENDED", "order": 1, "processInstanceId": 189406, '
        '"scriptName": "test1", "details": "Task OK", "startingDate": "2021-06-21 11:42:34.795359", '
        '"endingDate": "2021-06-21 11:42:35.108229", "newParameters": [] } ] }, "executorUsername": null }')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = response
        orch = orchestration_fixture
        assert orch.get_process_status_by_id(189406) == 'ENDED'
        assert orch.path == '/orchestration/v1/process-instance/189406'

    response_fail = ('[]')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = response_fail
        orch = orchestration_fixture
        assert orch.get_process_status_by_id(189406) is None
        assert orch.path == '/orchestration/v1/process-instance/189406'


def test_get_service_variable_by_name(orchestration_fixture):
    """
    Test Get Service Variables by Variable Name
    """

    device_info = ('{"TASKINSTANCEID":"353763"}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.get_service_variable_by_name('1234', 'TASKINSTANCEID')
        assert orch.path == \
            '/orchestration/service/variables/1234/TASKINSTANCEID'
        assert _is_valid_json(orch.response.text)


def test_update_service_variable(orchestration_fixture):
    """
    Update service variable
    """

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture
        orch.update_service_variable('1234', 'TASKINSTANCEID', 'NewValue')
        assert orch.path == \
            '/orchestration/service/variables/1234/TASKINSTANCEID?value=NewValue'
        mock_call_post.assert_called_once()


def test_delete_service_by_id(orchestration_fixture):
    """
    Delete service by ID
    """

    with patch('msa_sdk.msa_api.MSA_API._call_delete') as mock_call_delete:
        orch = orchestration_fixture
        orch.delete_service('1234')
        assert orch.path == '/orchestration/MSAA19224/service/instance/1234'
        mock_call_delete.assert_called_once()


def test_list_process_instances(orchestration_fixture):
    """
    Test list process instances
    """

    device_info = (
        '[{"processId":{"id":208606,"lastExecNumber":1,'
        '"name":"Fortigate_Ping_Execution/Process_Execute_Ping/Process_Execute_Ping",'
        '"submissionType":"RUN"},"serviceId":{"id":205732,'
        '"name":"Fortigate_Ping_Execution","serviceExternalReference":"FGT_PING",'
        '"state":null},"status":{"details":"Mandatory parameter device_id is not'
        'present","endingDate":"2017-06-04 15:18:00.0",'
        '"execNumber":1,'
        '"processTaskStatus":[{"details":"Mandatory parameter device_id is not present",'
        '"endingDate":"2017-06-04'
        '15:18:00.0","newParameter":[],"order":1,"processInstanceId":208606,'
        '"scriptName":"Execute Ping","startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}],'
        '"startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}}]')

    local_path = '/orchestration/process/instances/{}'.format(1234)

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.list_process_instances_by_service(1234)
        assert orch.path == local_path
        mock_call_get.assert_called_once()


def test_launch_process_instance(orchestration_fixture):
    """
    Test launch process instance
    """

    local_path = '/orchestration/process/execute/{}'
    local_path += '/{}?processName={}'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture
        orch.execute_launch_process_instance('1234', 'Process',
                                             {"var1": 1, "var2": 2})
        assert orch.path == local_path.format('MSAA19224', '1234',
                                              'Process')
        mock_call_post.assert_called_once()


def test_execute_service(orchestration_fixture):
    """
    Test execute service
    """

    local_path = '/orchestration/service/execute/{}'
    local_path += '?serviceName={}&processName={}&serviceInstance=0'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture
        orch.execute_service('1234', 'ProcessName',
                             {"var1": 1, "var2": 2})
        assert orch.path == local_path.format('MSAA19224', '1234',
                                              'ProcessName')
        mock_call_post.assert_called_once_with({"var1": 1, "var2": 2})


def test_execute_service_process(orchestration_fixture):
    """
    Test execute service process
    """

    local_path = '/orchestration/service/execute/{}'
    local_path += '?serviceName={}&processName={}&serviceInstance=0'

    result = ('{"serviceId": {'
              '"name": "Process/workflows/TestConPy/TestConPy",'
              '"id": 187201,'
              '"serviceExternalReference": "IOSSID187201",'
              '"state": null'
              '}, "processId": {'
              '"id": 189406, '
              '"name": "Process/workflows/TestConPy/Process_Test",'
              '"lastExecNumber": 1,'
              '"submissionType": "RUN"'
              '}}')

    with patch('requests.post') as mock_post:
        orch = orchestration_fixture

        mock_post.return_value.text = result

        assert orch.execute_service_process('1234', 'ProcessName',
                                            {"var1": 1, "var2": 2}) == (187201,
                                                                        189406)
        assert orch.path == local_path.format('MSAA19224', '1234',
                                              'ProcessName')


def test_execute_service_process_no_service_id(orchestration_fixture):
    """
    Test execute service process no service id
    """

    local_path = '/orchestration/service/execute/{}'
    local_path += '?serviceName={}&processName={}&serviceInstance=0'

    result = ('{"processId": {'
              '"id": 189406, '
              '"name": "Process/workflows/TestConPy/Process_Test",'
              '"lastExecNumber": 1,'
              '"submissionType": "RUN"'
              '}}')

    with patch('requests.post') as mock_post:
        orch = orchestration_fixture

        mock_post.return_value.text = result

        assert orch.execute_service_process('1234', 'ProcessName',
                                            {"var1": 1, "var2": 2}) == (-1,
                                                                        189406)
        assert orch.path == local_path.format('MSAA19224', '1234',
                                              'ProcessName')


def test_execute_service_process_no_process_id(orchestration_fixture):
    """
    Test execute service process no process id
    """

    local_path = '/orchestration/service/execute/{}'
    local_path += '?serviceName={}&processName={}&serviceInstance=0'

    result = ('{"serviceId": {'
              '"name": "Process/workflows/TestConPy/TestConPy",'
              '"id": 187201,'
              '"serviceExternalReference": "IOSSID187201",'
              '"state": null'
              '}}')

    with patch('requests.post') as mock_post:
        orch = orchestration_fixture

        mock_post.return_value.text = result

        assert orch.execute_service_process('1234', 'ProcessName',
                                            {"var1": 1, "var2": 2}) == (187201,
                                                                        -1)
        assert orch.path == local_path.format('MSAA19224', '1234',
                                              'ProcessName')


def test_execute_by_service(orchestration_fixture):
    """
    Test execute by service
    """

    local_path = '/orchestration/service/execute/{}'
    local_path += '/{}?serviceName={}&processName={}'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture
        orch.execute_by_service('external_ref', 'service_ref', 'serviceName',
                                'ProcessName',
                                {"var1": 1, "var2": 2})
        assert orch.path == local_path.format('external_ref', 'service_ref',
                                              'serviceName', 'ProcessName')
        mock_call_post.assert_called_once_with({"var1": 1, "var2": 2})


def test_execute_service_by_reference(orchestration_fixture):
    """
    Test execute service by reference
    """

    local_path = '/orchestration/service/execute/{}/{}'
    local_path += '?serviceName={}&processName={}'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture

        orch.execute_service_by_reference('external_ref', 'servReference',
                                          'servName', 'procName',
                                          {"var1": 1, "var2": 2})

        assert orch.path == local_path.format('external_ref', 'servReference',
                                              'servName', 'procName')

        mock_call_post.assert_called_once_with({"var1": 1, "var2": 2})


def test_list_process_instance_by_service_id(orchestration_fixture):
    """
    Test List process instance by service id
    """
    device_info = (
        '[{"processId":{"id":208606,"lastExecNumber":1,'
        '"name":"Fortigate_Ping_Execution/Process_Execute_Ping/Process_Execute_Ping",'
        '"submissionType":"RUN"},"serviceId":{"id":205732,'
        '"name":"Fortigate_Ping_Execution","serviceExternalReference":"FGT_PING",'
        '"state":null},"status":{"details":"Mandatory parameter device_id is not'
        'present","endingDate":"2017-06-04 15:18:00.0",'
        '"execNumber":1,'
        '"processTaskStatus":[{"details":"Mandatory parameter device_id is not present",'
        '"endingDate":"2017-06-04'
        '15:18:00.0","newParameter":[],"order":1,"processInstanceId":208606,'
        '"scriptName":"Execute Ping","startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}],'
        '"startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}}]')

    local_path = '/orchestration/process/instances/{}'.format(1234)

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.list_process_instances_by_service(1234)
        assert orch.path == local_path
        mock_call_get.assert_called_once()


def test_get_process_instance(orchestration_fixture):
    """
    Test get process instance
    """

    device_info = (
        '[{"processId":{"id":208606,"lastExecNumber":1,'
        '"name":"Fortigate_Ping_Execution/Process_Execute_Ping/Process_Execute_Ping",'
        '"submissionType":"RUN"},"serviceId":{"id":205732,'
        '"name":"Fortigate_Ping_Execution","serviceExternalReference":"FGT_PING",'
        '"state":null},"status":{"details":"Mandatory parameter device_id is not'
        'present","endingDate":"2017-06-04 15:18:00.0",'
        '"execNumber":1,'
        '"processTaskStatus":[{"details":"Mandatory parameter device_id is not present",'
        '"endingDate":"2017-06-04'
        '15:18:00.0","newParameter":[],"order":1,"processInstanceId":208606,'
        '"scriptName":"Execute Ping","startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}],'
        '"startingDate":"2017-06-04 15:18:00.0","status":"FAIL"}}]')

    local_path = '/orchestration/process/instance/{}'.format(1234)

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.get_process_instance(1234)
        assert orch.path == local_path
        mock_call_get.assert_called_once()


def test_update_process_script_details(orchestration_fixture):
    """
    Test update process script details
    """

    local_path = ('/orchestration/process/instance/{}'
                  '/task/{}/execnumber/{}/update').format(1234, 'Task-ID',
                                                          'exec-number')

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        orch = orchestration_fixture
        orch.update_process_script_details(1234, 'Task-ID', 'exec-number')
        assert orch.path == local_path
        mock_call_put.assert_called_once()


def test_update_service_instance_ref(orchestration_fixture):
    """
    Test update service instance reference
    """
    local_path = ('/orchestration/{}/service/instance/update'
                  '/{}/?serviceReference={}').format('MSAA19224', 'ServID',
                                                     'Serv_Ref')

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        orch = orchestration_fixture
        orch.update_service_instance_reference('ServID', 'Serv_Ref')
        assert orch.path == local_path
        mock_call_put.assert_called_once()


def test_read_service_instance(orchestration_fixture):
    """
    Test Read Service Instances
    """

    device_info = (
        '{"name":"Process/Reference/Customer/Kibana/kibana_dashboard",'
        '"id":2231,"serviceExternalReference":"MSASID2231","state":"ACTIVE"}')

    with patch('requests.get') as mock_call_get:
        mock_call_get.return_value.text = device_info
        orch = orchestration_fixture
        orch.read_service_instance('2231')
        assert orch.path == '/orchestration/MSAA19224/service/instance/2231'
        assert _is_valid_json(orch.response.text)


def test_update_asynchronous_task_details(orchestration_fixture):
    """
    Test update task async way
    """

    argument_dict = {
        'process_id': '1234',
        'task_id': '42',
        'exec_number': '4242',
        'data': 'Lorem ipsum dolor sit amet'}

    with patch('requests.put') as mock_call_put:
        assert not orchestration_fixture.update_asynchronous_task_details(
            **argument_dict)


def test_attach_wf_to_subtenant(orchestration_fixture):
    """
    Test attach_wf_to_subtenant
    """

    local_path = '/orchestration/service/attach'
    local_path += '?ubiqubeIds={}&uri={}'

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        orch = orchestration_fixture
        orch.attach_wf_to_subtenant("UBIA234", "Process/workflows/AutoAttached/organizations.xml")
        assert orch.path == local_path.format('UBIA234', 'Process/workflows/AutoAttached/organizations.xml')
        mock_call_post.assert_called_once_with()