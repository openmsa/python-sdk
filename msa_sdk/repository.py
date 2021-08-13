"""Module Repository."""


from urllib.parse import urlencode

from msa_sdk.msa_api import MSA_API


class Repository(MSA_API):
    """Class Repository."""

    def __init__(self):
        """Initialize."""
        MSA_API.__init__(self)
        self.api_path_v1 = "/repository/v1"
        self.api_path = "/repository"
        self.api_path_v2 = "/repository/v2"

    def file_update_comment(self, file_uri, comment):
        """
        File update document.

        Parameters
        ----------
        file_uri: String
            File path
        comment: Comment
            File comment

        Returns
        -------
        None

        """
        self.action = 'File update comment'
        url_encoded = urlencode({'uri': file_uri, 'comment': comment})

        self.path = "{}/comment?{}".format(self.api_path, url_encoded)

        self._call_post()

    def get_microservice_variables(self, file_uri):
        """
        Get microservice variables.

        Parameters
        ----------
            file_uri: String
            File path to microservice in repository
        Returns
        -------


        Dictionary: dict()
                    Dictionary wich contains microservice variables definition

        """
        import json
        self.action = 'Get variables for microservice'
        url_encoded = urlencode({'uri': file_uri})
        self.path = "{}/resource/variables?{}".format(
            self.api_path_v2, url_encoded)
        self._call_get()
        return json.loads(self.content)

    def post_repository_variables(self, respository_uri):
        """
        Get repository variables.

        Parameters
        ----------
        repository: String
            File path repository variables

        Returns
        -------
        None

        """
        self.action = 'Post repository variables'
        url_encoded = urlencode({'repository': respository_uri})

        self.path = "{}/variables?{}".format(self.api_path_v2, url_encoded)
        self._call_post()

    def get_microservice_details(self, file_uri):
        """
        Get microservice details.

        Parameters
        ----------
            file_uri: String
            File path to microservice in repository
        Returns
        -------


        Dictionary: dict()
            Dictionary wich contains microservice details

        """
        import json
        self.action = 'Get details for microservice'
        url_encoded = urlencode({'uri': file_uri})

        self.path = "{}/resource/microservice?{}".format(
            self.api_path_v2, url_encoded)

        self._call_get()
        return json.loads(self.content)

    def put_microservice_details(self, microservice_details):
        """
        Put microservice details.

        Parameters
        ----------
        file_uri: String
            File path to microservice in repository

        microservice_details: json
            JSON body of microservices detail

        Returns
        -------
        None

        """
        self.action = 'Put details of microservice'

        self.path = "{}/resource/microservice".format(self.api_path_v2)
        self._call_put(microservice_details)

    def create_microservice(self, microservice_details):
        """
        Create a new microservice.

        Parameters
        ----------
        microservice_details: json
            JSON body of microservices detail

        Returns
        -------
        None

        """
        self.action = 'Create a new microservice'

        self.path = "{}/resource/microservice".format(self.api_path_v2)
        self._call_post(microservice_details)

    def delete_repository_resource(self, file_uri):
        """
        Delete repository resource.

        Parameters
        ----------
        file_uri: String
            File path to microservice in repository

        Returns
        -------
        None

        """
        self.action = 'Delete repository resource'

        url_encoded = urlencode({'uri': file_uri})
        self.path = "{}/resource?{}".format(self.api_path_v2, url_encoded)
        self._call_delete()

    def get_microservice_path_by_name(self, microservice_name: str,
                                      deployment_settings_id: str):
        """
        Get MS file path by MS name and deployment settings ID.

        Parameters
        ----------
            microservice_name: Name of microservice
            depoloyment_settings_id: Deployment settings id

        Returns
        -------
        String: string
                Microservice file path or None

        """
        import re
        import json

        self.action = 'Get deployment settings'

        self.path = "/conf-profile/v2/{}".format(deployment_settings_id)
        self._call_get()
        result = json.loads(self.content)
        for microservice_path, microservice_details in \
                result['microserviceUris'].items():
            if re.search(microservice_name, microservice_path):
                return microservice_path
        else:
            return None

    def get_microservice_variables_default_value(self, file_uri: str) -> dict:
        """
        Get default values for microservice variables.

        Parameters
        ----------
            file_uri: Path to microservice file.
        Returns
        -------
            Dictionary: dict()
                        Variables and their default values

        """
        result = dict()
        self.action = 'Get variables default'
        variables = self.get_microservice_variables(file_uri)
        if 'variable' in list(variables.keys()):
            for variable_details in variables['variable']:
                result[variable_details['name'].replace(
                    'params.', '')] = variable_details['defaultValue']
        return result

    def detach_microserviceis_from_configuration_profile(
            self, deployment_settings_id: str, ms_list: list) -> None:
        """
        Detach microservice from configuration profile.

        Parameters
        ----------
            depoloyment_settings_id: Deployment settings id
            ms_list: List of microservice's URI to detach
        Returns
        -------
            None

        """
        import json
        self.action = 'Detach microservice from deployment settings'
        self.path = "/conf-profile/v2/detach/{}/repository/files".format(
            deployment_settings_id)
        self._call_put(json.dumps(ms_list))
        return None

    def get_workflow_definition(self, file_uri: str) -> dict:
        """
        Get workflow definition.

        Parameters
        ----------
            file_uri: Path to workflow file.
        Returns
        -------
            Dictionary: dict()
                        Variables and their default values

        """
        import json
        url_encoded = urlencode({'uri': file_uri})
        self.action = 'Get workflow definition'
        self.path = "/repository/v2/resource/workflow?{}".format(url_encoded)
        self._call_get()
        return json.loads(self.content)

    def change_workflow_definition(
            self,
            file_uri: str,
            workflow_definition_dict: dict) -> None:
        """
        Change workflow defenition.

        Parameters
        ----------
            file_uri: Path to workflow file
            workflow_definition_dict: Workflow definition
        Returns
        -------
            None

        """
        import json
        url_encoded = urlencode({'uri': file_uri})
        self.action = 'Change workflow definition'
        self.path = "/repository/v2/resource/workflow?{}".format(url_encoded)

        if not workflow_definition_dict['example']:
            workflow_definition_dict['example'] = dict()

        for process_details in workflow_definition_dict['process']:
            if not process_details['tasks']:
                process_details['tasks'] = list()

        self._call_put(json.dumps(workflow_definition_dict))
        return None

    def get_file(self, file_uri):
        """
        Get file content.

        Parameters
        ----------
            file_uri: String
            File path in repository
        Returns
        -------


        Dictionary: dict()
                    Dictionary wich contains file content

        """
        import json
        self.action = 'Get file content'
        url_encoded = urlencode({'uri': file_uri})
        self.path = "{}/file?{}".format(self.api_path, url_encoded)
        self.call_get()
        return json.loads(self.content)
