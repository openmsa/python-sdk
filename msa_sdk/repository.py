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

        self.call_post()

    def get_microservice_variables(self, file_uri):
        """
        Get microservice variables.

        Parameters
        ----------
        file_uri: String
            File path to microservice in repository

        Returns
        -------
        None

        """
        self.action = 'Get variables for microservice'
        url_encoded = urlencode({'uri': file_uri})

        self.path = "{}/resource/variables?{}".format(
            self.api_path_v2, url_encoded)
        self.call_get()

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
        self.call_post()

    def get_microservice_details(self, file_uri):
        """
        Get microservice details.

        Parameters
        ----------
        file_uri: String
            File path to microservice in repository

        Returns
        -------
        None

        """
        self.action = 'Get details for microservice'
        url_encoded = urlencode({'uri': file_uri})

        self.path = "{}/resource/microservice?{}".format(
            self.api_path_v2, url_encoded)
        self.call_get()

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
        self.call_put(microservice_details)

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
        self.call_post(microservice_details)


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
        self.call_delete()
