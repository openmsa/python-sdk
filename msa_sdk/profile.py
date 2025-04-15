import json
from msa_sdk.msa_api import MSA_API


class Profile(MSA_API):

    def __init__(self):
        MSA_API.__init__(self)
        self.api_path = "/profile"

    def exist(self, reference) -> bool:
        """

        Check if configuration profile exist by reference.

        Returns
        -------
        Boolean

        """
        self.action = 'Check Profile exist by reference'
        self.path = '{}/v1/exist/{}'.format(self.api_path, reference)
        self._call_post()
        result = json.loads(self.content)
        return result['exist']