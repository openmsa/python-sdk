"""
Test Repository
"""
from unittest.mock import patch
from urllib.parse import urlencode

from util import _is_valid_json
from util import microservice_info  # pylint: disable=unused-import
from util import repository_fixture

# pylint: disable=redefined-outer-name


def test_file_update_comment(repository_fixture):
    """
    Test file update comment
    """

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        repository = repository_fixture
        repository.file_update_comment(
            'Configuration/ABR/ABRA1570/FORTINET/timezone',
            'Comment value')

        data = urlencode({'uri': 'Configuration/ABR/ABRA1570/FORTINET/timezone',
                          'comment': 'Comment value'})

        assert repository.path == '/repository/comment?{}'.format(data)
        mock_call_post.assert_called_once_with()


def test_get_microservice_variables(repository_fixture):
    """
    Test get microservice variables.
    """
    response = ('{"variables" : {"variable" : [ {'
                '"defaultValue" : "1774", "displayName" : "Ansible server ME",'
                '"name" : "params.ansible_device_id"}]}}')

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        repository.get_microservice_variables(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )

        data = urlencode(
            {'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})
        assert repository.path == "/repository/v2/resource/variables?{}".format(
            data)
        mock_call_get.assert_called_once_with()


def test_post_repository_variables(repository_fixture):
    """
    Test post repository variables
    """

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        repository = repository_fixture
        repository.post_repository_variables(
            'fmc_repository'
        )

        data = urlencode({'repository': 'fmc_repository'})

        assert repository.path == "/repository/v2/variables?{}".format(data)
        mock_call_post.assert_called_once_with()


def test_get_microservice_details(repository_fixture):
    """
    Test get microservice details.
    """

    response = ('{"variables" : {"variable" : [ {'
                '"defaultValue" : "None", "displayName" : "Ansible server ME",'
                '"name" : "params.ansible_device_id"}]}}')

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        repository.get_microservice_details(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )

        data = urlencode(
            {'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/repository/v2/resource/microservice?{}".format(
            data)
        mock_call_get.assert_called_once_with()


def test_put_microservice_details(repository_fixture):
    """
    Test put microservice details.
    """

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        repository = repository_fixture
        ms_details = microservice_info()
        repository.put_microservice_details(ms_details)

        assert repository.path == "/repository/v2/resource/microservice"
        mock_call_put.assert_called_once()


def test_create_microservice(repository_fixture):
    """
    Test put microservice details.
    """

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        repository = repository_fixture
        ms_details = microservice_info()
        repository.create_microservice(ms_details)

        assert repository.path == "/repository/v2/resource/microservice"
        mock_call_post.assert_called_once()


def test_delete_repository_resource(repository_fixture):
    """
    Delete repository resource.
    """

    with patch('msa_sdk.msa_api.MSA_API._call_delete') as mock_call_delete:
        repository = repository_fixture
        repository.delete_repository_resource(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )

        data = urlencode(
            {'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/repository/v2/resource?{}".format(data)
        mock_call_delete.assert_called_once


def test_get_microservice_path_by_name(repository_fixture):
    """
    Test get microservice file path by microservice name
    and deployment settings ID.
    """

    response = (
        '{"microserviceUris": {"CommandDefinition/ANSIBLE/Retrieve_playbook_files_list.xml":'
        ' {"name": "Retrieve playbook files list","groups": ["Default"]},'
        '"CommandDefinition/ANSIBLE/Read_playbook_file.xml": {"name": "Read playbook file",'
        '"groups": ["Default"]},"CommandDefinition/ANSIBLE/Read_hosts_file.xml": {"name": '
        '"Read hosts file","groups": ["Default"]}}}')

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_microservice_path_by_name(
            'Read_playbook_file.xml',
            '276') == 'CommandDefinition/ANSIBLE/Read_playbook_file.xml'
        assert repository.get_microservice_path_by_name('test', '276') is None


def test_get_microservice_variables_default_value(repository_fixture):
    """
    Test get default values for microservice variables.
    """

    response = ('{"variable" : [ {'
                '"defaultValue" : "1774", "displayName" : "Ansible server ME",'
                '"name" : "params.ansible_device_id"}]}')

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_microservice_variables_default_value(
            'CommandDefinition/ANSIBLE/Read_playbook_file.xml') == {"ansible_device_id": "1774"}


def test_detach_microserviceis_from_configuration_profile(repository_fixture):
    """
    Test detach microservice from configuration profile.
    """

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        repository = repository_fixture
        repository.detach_microserviceis_from_configuration_profile(
            '276', ['CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'], )

        data = urlencode(
            {'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/conf-profile/v2/detach/276/repository/files"


def test_get_workflow_definition(repository_fixture):
    """
    Test Get workflow definition.
    """

    #response = '{"variables": {"variable": [{"defaultValue": "name1", "displayName": "var_name", "name": "params.var_name", "startIncrement": 0, "type": "String", "mandatoryArray": False, "visible": True, "description": "", "groupSeparator": "", "groupDisplayName": "", "displayOrder": 0, "increment": 0, "refServiceURI": "", "refDeviceIdVar": None, "keepOnImport": False, "editable": False, "onlyDetailView": False, "localVarNameMatch": "", "remoteVarNameMatch": "", "arrayCanAdd": True, "arrayCanRemove": True, "arrayCanMove": True, "arrayCanEdit": True, "mandatory": False, "userLocked": False, "grouped": False, "searchable": False, "uniqueGlobal": False, "selector": None, "defaultValueLong": None, "displayNameHeader": "", "fullDisplayName": "", "behaviour": None, "indexVariables": None, "sections": None, "sdTypes": None, "class": None, "values": None}, {"defaultValue": "24", "displayName": "integer", "name": "params.integer", "startIncrement": 0, "type": "Integer", "mandatoryArray": False, "visible": True, "description": "", "groupSeparator": "", "groupDisplayName": "", "displayOrder": 0, "increment": 0, "refServiceURI": "", "refDeviceIdVar": None, "keepOnImport": False, "editable": False, "onlyDetailView": False, "localVarNameMatch": "", "remoteVarNameMatch": "", "arrayCanAdd": True, "arrayCanRemove": True, "arrayCanMove": True, "arrayCanEdit": True, "mandatory": False, "userLocked": False, "grouped": False, "searchable": False, "uniqueGlobal": False, "selector": None, "defaultValueLong": None, "displayNameHeader": "", "fullDisplayName": "", "behaviour": None, "indexVariables": None, "sections": None, "sdTypes": None, "class": None, "values": None}, {"defaultValue": None, "displayName": "array_array", "name": "params.array_array", "startIncrement": 0, "type": "String", "mandatoryArray": False, "visible": True, "description": "", "groupSeparator": "", "groupDisplayName": "", "displayOrder": 0, "increment": 0, "refServiceURI": "", "refDeviceIdVar": None, "keepOnImport": False, "editable": False, "onlyDetailView": False, "localVarNameMatch": "", "remoteVarNameMatch": "", "arrayCanAdd": True, "arrayCanRemove": True, "arrayCanMove": True, "arrayCanEdit": True, "mandatory": False, "userLocked": False, "grouped": False, "searchable": False, "uniqueGlobal": False, "selector": None, "defaultValueLong": None, "displayNameHeader": "", "fullDisplayName": "", "behaviour": None, "indexVariables": None, "sections": None, "sdTypes": None, "class": None, "values": None}], "frozen": 0}, "example": None, "process": [{"name": "Process/workflows/TEST_WF1/Process_instanciate", "displayName": "instanciate", "type": "CREATE", "visibility": 5, "allowSchedule": None, "tasks": [{"displayName": "instanciate", "fileName": "Task_instanciate.py", "fileUri": "/opt/fmc_repository/Process/workflows/TEST_WF1/Process_instanciate/Tasks"}]}, {"name": "Process/workflows/TEST_WF1/Process_update_array", "displayName": "update_array", "type": "UPDATE", "visibility": 5, "allowSchedule": None, "tasks": [{"displayName": "update_array", "fileName": "Task_update_array.py", "fileUri": "/opt/fmc_repository/Process/workflows/TEST_WF1/Process_update_array/Tasks"}]}], "information": {"displayName": "TEST_WF1", "icon": None, "description": "TEST_WF1", "category": None, "displayField": "service_id", "serviceTaskType": "python", "order": 10000, "visibility": 5}, "metaInformationList": [{"type": "FILE", "name": "TEST_WF1.xml", "displayName": "TEST_WF1.xml", "repositoryName": "Process", "parentURI": "Process/workflows/TEST_WF1", "fileType": "text", "tag": None, "comment": None, "modelId": 0, "vendorId": 0, "uri": "Process/workflows/TEST_WF1/TEST_WF1.xml", "file": True}]}'
    
    response = (
        '{"information" : {"displayName" : "Execute Get workflow definition"}}')
                
    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_workflow_definition('Process/workflows/TEST_WF1/TEST_WF1.xml')[
             'information']['displayName'] == 'Execute Get workflow definition'            

def test_change_workflow_definition(repository_fixture):
    """
    Test change workflow definition.
    """

    with patch('msa_sdk.msa_api.MSA_API._call_put') as mock_call_put:
        repository = repository_fixture
        assert repository.change_workflow_definition('Execute_Ansible_based_microservice.xml', {
                                                     "example": "", "process": [{"tasks": ""}]}) is None


def test_create_workflow_definition(repository_fixture):
    """
    Test create workflow definition.
    """
    
    import json
    workflow_definition =  ''' {
                  "example": {
                    "content": "string"
                  },
                  "metaInformationList": [
                    {
                      "type": "FILE",
                      "name": "TEST_NEW_WF.xml",
                      "displayName": "TEST_NEW_WF",
                      "repositoryName": "Process",
                      "parentURI": "Process/workflows/TEST_NEW_WF",
                      "fileType": "text",
                      "tag": "string",
                      "comment": "string",
                      "modelId": 0,
                      "vendorId": 0,
                      "uri": "Process/workflows/TEST_NEW_WF/TEST_NEW_WF.xml",
                      "file": "true"
                    }
                  ],
                  "information": {
                    "displayName": "TEST_NEW_WF",
                    "icon": "string",
                    "description": "TEST_NEW_WF",
                    "category": "string",
                    "displayField": "string",
                    "serviceTaskType": "string",
                    "order": 0,
                    "visibility": "5"
                  },
                  "process": [
                    {
                      "name": "Process/workflows/TEST_NEW_WF/create",
                      "displayName": "instanciate",
                      "type": "CREATE",
                      "visibility": "5",
                      "allowSchedule": false,
                      "tasks": [
                        {
                          "fileName": "Task1.py",
                          "fileUri": "/opt/fmc_repository/Process/workflows/TEST_NEW_WF/Process_instanciate/Tasks",
                          "displayName": "Task1"
                        }
                      ]
                    }
                  ]
                } 
         '''
    workflow_definition_dict = json.loads(workflow_definition)  #convert string into dict

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        repository = repository_fixture
        assert repository.create_workflow_definition(workflow_definition_dict) is None

def test_create_workflow_definition2(repository_fixture):
    """
    Test create workflow definition with empty workflow_definition_dict['process']['tasks'].
    """
    
    import json
    workflow_definition =  ''' {
                  "example": {
                    "content": "string"
                  },
                  "metaInformationList": [
                    {
                      "type": "FILE",
                      "name": "TEST_NEW_WF.xml",
                      "displayName": "TEST_NEW_WF",
                      "repositoryName": "Process",
                      "parentURI": "Process/workflows/TEST_NEW_WF",
                      "fileType": "text",
                      "tag": "string",
                      "comment": "string",
                      "modelId": 0,
                      "vendorId": 0,
                      "uri": "Process/workflows/TEST_NEW_WF/TEST_NEW_WF.xml",
                      "file": "true"
                    }
                  ],
                  "information": {
                    "displayName": "TEST_NEW_WF",
                    "icon": "string",
                    "description": "TEST_NEW_WF",
                    "category": "string",
                    "displayField": "string",
                    "serviceTaskType": "string",
                    "order": 0,
                    "visibility": "5"
                  },
                  "process": [
                    {
                      "name": "Process/workflows/TEST_NEW_WF/create",
                      "displayName": "instanciate",
                      "type": "CREATE",
                      "visibility": "5",
                      "allowSchedule": false,
                      "tasks": []
                    }
                  ]
                } 
         '''
    workflow_definition_dict = json.loads(workflow_definition)  #convert string into dict

    with patch('msa_sdk.msa_api.MSA_API._call_post') as mock_call_post:
        repository = repository_fixture
        assert repository.create_workflow_definition(workflow_definition_dict) is None


def test_delete_workflow_definition(repository_fixture):
    """
    Test delete workflow definition.
    """

    response = ('{}')

    with patch('msa_sdk.msa_api.MSA_API._call_delete') as mock_call_delete:
        repository = repository_fixture
        repository._content = response
        assert repository.delete_workflow_definition('Process/workflows/TEST_WF1/TEST_WF1.xml') is None


def test_get_file(repository_fixture):
    """
    Test get file.
    """
    response = ('{"content" : "<?php\\n\\n////test;\\n?>" }')

    with patch('msa_sdk.msa_api.MSA_API._call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        repository.get_file('Datafiles/test.php')

        data = urlencode(
            {'uri': 'Datafiles/test.php'})
        assert repository.path == "/repository/file?{}".format(
            data)
        mock_call_get.assert_called_once_with()

