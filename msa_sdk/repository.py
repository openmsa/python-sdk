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
