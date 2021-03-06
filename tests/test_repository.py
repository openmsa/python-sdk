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

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
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

    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        repository.get_microservice_variables(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )
        
        data = urlencode({'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})
        assert repository.path == "/repository/v2/resource/variables?{}".format(data)
        mock_call_get.assert_called_once_with()

def test_post_repository_variables(repository_fixture):
    """
    Test post repository variables
    """

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        repository = repository_fixture
        repository.post_repository_variables(
            'fmc_repository'
        )

        data = urlencode({'repository':'fmc_repository'})

        assert repository.path == "/repository/v2/variables?{}".format(data)
        mock_call_post.assert_called_once_with()

def test_get_microservice_details(repository_fixture):
    """
    Test get microservice details.
    """

    response = ('{"variables" : {"variable" : [ {'
            '"defaultValue" : "None", "displayName" : "Ansible server ME",'
            '"name" : "params.ansible_device_id"}]}}')

    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        repository.get_microservice_details(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )
        
        data = urlencode({'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/repository/v2/resource/microservice?{}".format(data)
        mock_call_get.assert_called_once_with()

def test_put_microservice_details(repository_fixture):
    """
    Test put microservice details.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        repository = repository_fixture
        ms_details = microservice_info()
        repository.put_microservice_details(ms_details)

        assert repository.path == "/repository/v2/resource/microservice"
        mock_call_put.assert_called_once()

def test_create_microservice(repository_fixture):
    """
    Test put microservice details.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_post') as mock_call_post:
        repository = repository_fixture
        ms_details = microservice_info()
        repository.create_microservice(ms_details)

        assert repository.path == "/repository/v2/resource/microservice"
        mock_call_post.assert_called_once()

def test_delete_repository_resource(repository_fixture):
    """
    Delete repository resource.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_delete') as mock_call_delete:
        repository = repository_fixture
        repository.delete_repository_resource(
            'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'
        )

        data = urlencode({'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/repository/v2/resource?{}".format(data)
        mock_call_delete.assert_called_once

def test_get_microservice_path_by_name(repository_fixture):
    """
    Test get microservice file path by microservice name 
    and deployment settings ID.
    """

    response = ('{"microserviceUris": {"CommandDefinition/ANSIBLE/Retrieve_playbook_files_list.xml":'
                ' {"name": "Retrieve playbook files list","groups": ["Default"]},'
                '"CommandDefinition/ANSIBLE/Read_playbook_file.xml": {"name": "Read playbook file",'
                '"groups": ["Default"]},"CommandDefinition/ANSIBLE/Read_hosts_file.xml": {"name": '
                '"Read hosts file","groups": ["Default"]}}}')

    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_microservice_path_by_name('Read_playbook_file.xml', '276') == 'CommandDefinition/ANSIBLE/Read_playbook_file.xml'
        assert repository.get_microservice_path_by_name('test', '276') == None

def test_get_microservice_variables_default_value(repository_fixture):
    """
    Test get default values for microservice variables.
    """

    response = ('{"variable" : [ {'
                '"defaultValue" : "1774", "displayName" : "Ansible server ME",'
                '"name" : "params.ansible_device_id"}]}')


    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_microservice_variables_default_value('CommandDefinition/ANSIBLE/Read_playbook_file.xml') == {"ansible_device_id": "1774"}

def test_detach_microserviceis_from_configuration_profile(repository_fixture):
    """
    Test detach microservice from configuration profile.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        repository = repository_fixture
        repository.detach_microserviceis_from_configuration_profile(
            '276', ['CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'], 
        )

        data = urlencode({'uri': 'CommandDefinition/Reference/AWS/Generic/EC2/instances.xml'})

        assert repository.path == "/conf-profile/v2/detach/276/repository/files"

def test_get_workflow_definition(repository_fixture):
    """
    Test Get workflow definition.
    """

    response = ('{"information" : {"displayName" : "Execute Ansible-based microservice"}}')

    with patch('msa_sdk.msa_api.MSA_API.call_get') as mock_call_get:
        repository = repository_fixture
        repository._content = response
        assert repository.get_workflow_definition('Execute_Ansible_based_microservice.xml')['information']['displayName'] == 'Execute Ansible-based microservice'

def test_change_workflow_definition(repository_fixture):
    """
    Test change workflow defenition.
    """

    with patch('msa_sdk.msa_api.MSA_API.call_put') as mock_call_put:
        repository = repository_fixture
        assert repository.change_workflow_definition('Execute_Ansible_based_microservice.xml', {"example": "", "process": [{"tasks": ""}]}) == None
